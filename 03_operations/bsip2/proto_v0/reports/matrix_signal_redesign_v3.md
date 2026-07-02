# Component B Matrix Signal — Redesign Addendum v3
**Proposal Class:** D6 (Nutrition Agent — scoring formula redesign)
**Required co-sign:** Product Agent (D7) — formula behavior change, affects ranking of live categories; required before Data Agent may implement
**Task:** TASK-395
**Date authored:** 2026-06-25
**Status:** PROPOSAL ONLY — no engine code changed, no scores changed, no published score affected
**Supersedes (partially):** §2.5 formula of `matrix_signal_redesign_v2.md` (the v4 formula that cleared B1/B3 but not B2)
**Depends on:** `shared_reader_build_v1.md` v4 section (reading layer fixed, independently QA-verified by agent aae16ab1101f71f68)

---

## 1. What This Document Addresses

The v4 probe cleared Gate B1 (96.8%) and Gate B3 (100%) but failed Gate B2 (75%, bar 95%). Independent QA (agent aae16ab1101f71f68) confirmed the B2 failure is a formula design gap, not a reading problem. Three pairs of products tie at score 52.5 despite one product being clearly more whole-food-dense than the other:

| Pair | Products | v4 Result | Root Cause |
|---|---|---|---|
| RP-03 | oats 47% direct vs oats 38% + nuts 4.7% | 52.5 vs 52.5 tie | Dead zone + non-grain whole over-credit |
| RP-04 | granola oats 28% effective vs oats 39% direct | 52.5 vs 52.5 tie | Dead zone + gold-set annotation error |
| RP-08 | oats 47% direct vs oats 39% + raisins pos-only | 52.5 vs 52.5 tie | Dead zone + non-grain whole over-credit |

This addendum fixes all three with two targeted formula changes and rules on the gold-set annotation for RP-04.

---

## 2. Root Cause: The Anchor Dead Zone

The v4 formula applies an anchor nudge: when the highest-weight marker is a whole ingredient and the raw dominance ratio is below 0.5, the ratio is boosted by +0.15, capped at 0.5. This creates a structural dead zone:

```
raw dom_ratio in [0.35, 0.50) + anchor=whole  =>  adj_ratio = min(0.50, raw+0.15) = 0.50 always
                                               =>  score = 10 + 0.50 * 85 = 52.5 always
```

Any mixed product whose whole-food weight falls between 35% and 50% of total marked weight — and whose heaviest single marker is a grain — locks to exactly 52.5. In the mixed band this affects a large set of genuinely different products. A product with 47% oats and one with 38% oats both have raw dom_ratios in this range; the +0.15 boost clamps both to 0.50.

The fix has two components, both required together: reduce the anchor nudge to shrink the dead zone, and apply a grain-context penalty to non-grain whole contributors so they do not inflate dominance ratios in grain-primary products.

---

## 3. Change 1: Non-Grain Whole Weighting in Grain-Context Products (M-2 rule)

### 3.1 Nutrition Rationale

The matrix signal's purpose is to measure **whole-food vs refined-starch matrix character**. In a grain-primary product (oat muesli, granola, grain-based snack bar), the structural driver is the grain fraction. Nuts, seeds, and dried fruit are add-ins. They are genuine whole foods but they are on a different nutritional axis than grain completeness:

- Nuts contribute fat, protein, and micronutrients — not grain fiber, grain starch complexity, or whole-grain phytonutrient profile.
- Raisins and dates contribute simple sugars (concentrated fructose/glucose) with some fiber. They are nutritionally intermediate — better than refined sugar but not equivalent to intact grain.
- Seeds (sesame, chia, flax) contribute fat and micronutrients similar to nuts.

When the signal is being used to distinguish "47% whole oats first" from "38% whole oats + 4.7% nuts," counting nuts at full value on the whole-food side is incorrect. A consumer reading the label correctly understands that 47% oats is a more grain-dense product than 38% oats regardless of the nut add-in. The nut add-in is orthogonal to grain density.

The signal is not a comprehensive whole-food quality signal — it is specifically the **grain matrix signal**. Non-grain whole contributors should receive partial credit in this context, not equal credit.

**Evidence tier: Moderate.** This is a principled classification decision grounded in macronutrient function, not a measurement from a controlled trial. The corpus confirms the practical consequence: without a grain-context penalty, 4.7% nuts at position 6 (stated pct) adds enough whole-weight to tie a product with 9 additional percentage points of oats.

### 3.2 The Rule

In any product where at least one **grain whole marker** is present, all **non-grain whole markers** receive a 0.5x weight discount.

**Grain whole markers** (eligible to trigger grain context):
`whole_wheat_flour`, `whole_wheat_grain`, `whole_spelt_flour`, `whole_spelt_grain`, `whole_oat_flour`, `whole_oat`, `whole_oat_flakes`, `whole_rye_flour`, `whole_rye_grain`, `whole_corn_flour`, `whole_barley_flour`, `whole_rice`, `oat_groats`, `hulled_oats`, `oat_flakes_plain`, `quinoa`, `buckwheat`, `bare_wheat_first_80pct`

**Non-grain whole markers** (subject to 0.5x discount when grain context is present):
`nuts`, `almonds`, `peanuts`, `pistachios`, `cashews`, `seeds_specific`, `seeds_generic`, `sesame_seeds`, `chia_seeds`, `flax_seeds`, `dates`, `raisins`, `tahini`, `olive_oil`, `butter_dairy`, `sourdough_starter`

Note: `barley_malt` already carries `half_weight=True` in the existing lexicon — it is already discounted and is NOT double-discounted by this rule.

**When grain context is absent** (a pure nut/seed/fruit product, or a product with only refined grain markers): all whole markers receive full weight. The 0.5x applies only inside grain-primary products.

### 3.3 Worked Numbers: RP-03 (47% oats vs 38% oats + nuts 4.7%)

**Product A — oats 47% direct** (barcode 7290016883176):
- oat_flakes_plain: stated_pct=47.0, eff_w=0.4700 (grain whole, grain context active)
- sugar pos=3: eff_w=0.1465
- veg_oil pos=4: eff_w=0.1185
- glucose_syrup pos=5: eff_w=0.0948
- glucose pos=5: eff_w=0.0948
- refined_wheat_flour pos=6: eff_w=0.0754
- `whole_w=0.4700, refined_w=0.5300`
- raw dom_ratio = 0.4700/1.0000 = 0.4700
- anchor = oat_flakes_plain (whole), nudge = min(0.50, 0.4700+0.05) = 0.5000
- **Score = 10 + 0.50 * 85 = 52.5**

**Product B — oats 38% + nuts 4.7%** (barcode 7290011131371):
- oat_flakes_plain: stated_pct=38.0, eff_w=0.3800 (grain whole, grain context active)
- veg_oil pos=2: eff_w=0.1541
- sugar pos=3: eff_w=0.1278
- glucose_syrup pos=4: eff_w=0.1034
- glucose pos=4: eff_w=0.1034
- refined_wheat_flour pos=5: eff_w=0.0827
- nuts: stated_pct=4.7, base_w=0.0470, **0.5x grain penalty** -> eff_w=0.0235
- peanuts: stated_pct=0.127, base_w=0.00127, **0.5x penalty** -> eff_w=0.0006
- almonds: stated_pct=0.047, base_w=0.00047, **0.5x penalty** -> eff_w=0.0002
- `whole_w=0.4044, refined_w=0.5713`
- raw dom_ratio = 0.4044/0.9757 = 0.4145
- anchor = oat_flakes_plain (whole), nudge = min(0.50, 0.4145+0.05) = 0.4645
- **Score = 10 + 0.4645 * 85 = 49.5**

**Result: 52.5 > 49.5. RP-03 PASSES.**

---

## 4. Change 2: Anchor Nudge Reduced from +/-0.15 to +/-0.05 (M-1 rule — dead zone fix)

### 4.1 Rationale

Even after applying the grain-context penalty, RP-08 (47% oats vs 39% oats + raisins by position) would remain a tie without reducing the anchor nudge. The 39%-oat product's raw dom_ratio after grain-penalty would be 0.4443; adding +0.15 still caps at 0.50; the 47%-oat product is already at dom_ratio 0.47 and also caps at 0.50. Both score 52.5.

The large +0.15 anchor nudge was designed to give a meaningful prior to the dominant first ingredient. With the full +0.15, anything in the raw dom_ratio band [0.35, 0.50) — a 15-point wide range — collapses to a single score. This destroys the formula's ability to rank products within the mixed band, which is precisely where B2 pairs live.

Reducing the nudge to +/-0.05 shrinks the dead zone to raw dom_ratio [0.45, 0.50). Products with 47% oats land at dom_ratio=0.47, which with a +0.05 nudge reaches exactly 0.50 (score=52.5). Products with 39% oats land at dom_ratio=0.44, which with a +0.05 nudge reaches 0.49 (score=52.0). The 0.5-point separation is narrow but real.

The anchor's residual purpose — providing a modest prior for the dominant first ingredient — is preserved. The 47% oat product still benefits slightly from the anchor (raw 0.47 -> adj 0.50); the 39% oat product benefits less (raw 0.44 -> adj 0.49). Products with very low raw dom_ratio (0.35, meaning only 35% of marked weight is whole-food) would get adj 0.40, yielding score=44.0 — meaningfully below the midpoint.

**What the anchor change does NOT do:** it does not remove the monotonicity guarantee. A product with more whole-food weight always produces a higher or equal dominance ratio, which always produces a higher or equal score. The anchor is a directional nudge bounded by the 0.5 cap; it cannot invert the direction.

### 4.2 Dead Zone Comparison

| raw dom_ratio | v4 adj (nudge +0.15) | v4 score | v5 adj (nudge +0.05) | v5 score |
|---|---|---|---|---|
| 0.35 | 0.50 | 52.5 | 0.40 | 44.0 |
| 0.40 | 0.50 | 52.5 | 0.45 | 48.2 |
| 0.44 | 0.50 | 52.5 | 0.49 | 52.0 |
| 0.47 | 0.50 | 52.5 | 0.50 | 52.5 |
| 0.49 | 0.50 | 52.5 | 0.50 | 52.5 |
| 0.52 | 0.52 | 54.2 | 0.52 | 54.2 |

Under v5, only products with raw dom_ratio in [0.45, 0.50) are affected by the cap — a 5-point band vs the 15-point band of v4.

### 4.3 Worked Numbers: RP-08 (47% oats vs 39% oats + raisins)

**Product A — oats 47%** (same as §3.3 Product A): Score = 52.5

**Product C — oats 39% + raisins position-only** (barcode 7290011131388):
- oat_flakes_plain: stated_pct=39.0, eff_w=0.3900 (grain whole, grain context active)
- veg_oil pos=2: eff_w=0.1761
- sugar pos=3: eff_w=0.1461
- glucose_syrup pos=4: eff_w=0.1181
- refined_wheat_flour pos=5: eff_w=0.0945
- raisins pos=6: no stated_pct, base_w by position=0.0752, **0.5x grain penalty** -> eff_w=0.0376
- `whole_w=0.4276, refined_w=0.5348`
- raw dom_ratio = 0.4276/0.9624 = 0.4443
- anchor = oat_flakes_plain (whole), nudge = min(0.50, 0.4443+0.05) = 0.4943
- **Score = 10 + 0.4943 * 85 = 52.0**

**Result: 52.5 > 52.0. RP-08 PASSES.**

---

## 5. Ruling on RP-04 Gold-Set Annotation (H-1 finding)

### 5.1 The RP-04 Claim

RP-04 asserts:
- **Higher product**: 7290011131975 (גרנולה פירות) — oats 43% within granola composite 65%, giving effective product-weight oats = 43% × 65% = 27.95%
- **Lower product**: 7290011131388 (מוזלי קראנצי תפוח קינמון) — oats 39% direct stated product-weight

The gold set's RP-04 label was set before the reading fix, when the reader could not correctly compute the granola's effective oat percentage (the parent composite had no stated_pct, so effective_pct=None). The annotation reflected an intuition that "43% oats in the granola" sounded like more oat content than "39% oats."

### 5.2 The Nutritional Ruling

**The gold-set RP-04 direction is incorrect. The 39%-direct product should rank higher than the 28%-effective product.**

The reasoning:

**Mass comparison is the ground truth.** The metric is measuring whole-food mass contribution relative to total product weight. 27.95% effective oats (by product weight) is simply less oat mass per gram of product than 39% direct oats. The granola composite also contains within it: refined wheat flour, vegetable oil, sugar, refined corn flour, glucose syrup — all of which are refined markers. After the reading fix, these correctly reduce the granola's whole-food fraction.

**The composite frame does not rescue the claim.** The intuition "43% of the granola is oats" is true at the granola level but misleading at the product level. The granola itself is only 65% of the product. The oat fraction of the final product is 43% × 65% = 27.95%. A consumer eating 100g of this product eats approximately 28g of oats. A consumer eating 100g of the 39%-oat muesli eats approximately 39g of oats. The muesli delivers more whole grain per gram of product.

**"Effective fraction" is not a premium.** The fact that oats are measured as a fraction of the granola sub-composite does not confer nutritional superiority. Both percentages express what is actually in the product. The granola's 65% composite includes a substantial refined component that dilutes the oat contribution.

**The reading fix confirmed what was always true.** The v4 reader correctly computes the effective oat percentage as 27.95%. The formula correctly scores the 39%-oat product higher. The pre-fix annotation was based on a broken computation, not a deliberate nutritional judgment.

### 5.3 Gold-Set Correction

RP-04 must be inverted in the gold-set JSON:
- `"higher": "7290011131388"` (oats 39% direct — the muesli)
- `"lower": "7290011131975"` (oats 27.95% effective — the granola)

**This is a gold-set correction, not a formula accommodation.** The formula correctly implements the nutritional logic. The annotation was wrong.

Under v5 with this correction, the pair result is: granola scores 45.6, muesli scores 52.0. The corrected direction passes.

**Flagged for QA re-review.** Per instructions, this gold-set correction must be re-reviewed by independent QA. The Nutrition Agent asserts the nutritional reasoning above as the basis; QA should verify whether the reasoning is sound and whether the formula's output is consistent with label-reading judgment.

---

## 6. The v5 Formula — Implementable Pseudocode

```python
# Classification sets for grain-context determination
GRAIN_WHOLE_LABELS = {
    "whole_wheat_flour", "whole_wheat_grain",
    "whole_spelt_flour", "whole_spelt_grain",
    "whole_oat_flour", "whole_oat", "whole_oat_flakes",
    "whole_rye_flour", "whole_rye_grain",
    "whole_corn_flour", "whole_barley_flour", "whole_rice",
    "oat_groats", "hulled_oats", "oat_flakes_plain",
    "quinoa", "buckwheat", "bare_wheat_first_80pct",
}

NON_GRAIN_WHOLE_LABELS = {
    "nuts", "almonds", "peanuts", "pistachios", "cashews",
    "seeds_specific", "seeds_generic", "sesame_seeds",
    "chia_seeds", "flax_seeds",
    "dates", "raisins",
    "tahini", "olive_oil", "butter_dairy", "sourdough_starter",
}
# NOTE: barley_malt is already half_weight=True in the lexicon;
# it is NOT additionally discounted by the grain-context rule.


def compute_component_b_score_v5(markers: list[dict]) -> Optional[float]:
    """
    v5 formula — two changes from v4:
      1. Non-grain whole markers receive 0.5x weight in grain-context products.
      2. Anchor nudge is +/-0.05 (was +/-0.15).

    Input markers: same schema as v4 — dicts with:
      label (str), class ("whole"|"refined"), position (int|None),
      stated_pct (float|None), half_weight (bool).
    """
    if not markers:
        return None

    # Determine grain context
    has_grain_whole = any(
        m["label"] in GRAIN_WHOLE_LABELS
        for m in markers if m["class"] == "whole"
    )

    # Separate stated-pct markers from position-only markers
    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]

    # Compute stated mass fraction and remaining mass
    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    total_stated_pct = min(total_stated_pct, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)

    # Compute total position weight for distributing remaining mass
    total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)

    def effective_weight(m: dict) -> float:
        # Base weight: stated_pct or position-distributed share of remaining mass
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            if total_pos_weight > 0:
                w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass
            else:
                w = 0.0

        # Apply lexicon half-weight modifier (e.g. barley_malt)
        if m.get("half_weight"):
            w *= 0.5

        # v5 change 1: grain-context penalty for non-grain whole contributors
        if (has_grain_whole
                and m["class"] == "whole"
                and m["label"] in NON_GRAIN_WHOLE_LABELS):
            w *= 0.5

        return w

    # Compute weighted whole and refined sums
    whole_weight   = sum(effective_weight(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(effective_weight(m) for m in markers if m["class"] == "refined")

    total_weight = whole_weight + refined_weight
    if total_weight < 0.01:
        return None  # No markers — caller applies MD-2 pessimistic fallback

    # Dominance ratio: fraction of marked weight that is whole-food
    dominance_ratio = whole_weight / total_weight

    # First-ingredient anchor
    highest_weight_marker = max(markers, key=effective_weight)
    anchor_class = highest_weight_marker["class"]

    # v5 change 2: reduced anchor nudge (+/-0.05, was +/-0.15)
    ANCHOR_NUDGE = 0.05
    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - ANCHOR_NUDGE)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + ANCHOR_NUDGE)

    # Map to [0, 100] — unchanged endpoint mapping
    score = 10.0 + dominance_ratio * 85.0

    return round(score, 1)
```

**What is not changed from v4:**
- `_pos_weight()` curve — identical
- Lexicon (MARKERS) — identical to v4
- `extract_all_markers_v4()` — identical (reading layer unchanged)
- `effective_weight()` stated-pct vs position-weight logic — identical, plus the two new modifiers
- Score endpoint mapping (`10 + dr * 85`) — identical
- Anchor cap direction logic — identical, only the nudge magnitude changes

---

## 7. Validation Results (Pre-Implementation Simulation)

The v5 formula was simulated on the full gold set using the exact v4 marker extractions (reading layer unchanged). Results:

| Gate | v4 | v5 | Bar |
|---|---|---|---|
| B1 anchor calibration | PASS 96.8% [30/31] | PASS 96.8% [30/31] | >=90% |
| B2 ordinal ranking | FAIL 75.0% [9/12] | **PASS 100.0% [12/12]** | >=95% |
| B3 coverage | PASS 100.0% [55/55] | PASS 100.0% [55/55] | >=95% |

B2 passes at 100% because the one genuinely failing pair (RP-04) is resolved by the gold-set correction, not by the formula. The formula correctly produces the right direction (muesli 52.0 > granola 45.6); it was the gold-set annotation that was wrong.

B1 still has one failure: barcode 7290106571945 (tier=T1, score=54.1). This is unchanged from v4 — it is the composite-without-parent-pct design gap (a `דגנים` parent with no stated_pct; sub-percentages 41% and 4.5% are product-weight but cannot participate in the effective_pct multiplication). This is a remaining formula gap, not a regression under v5.

**Simulation artifacts** (for verification):
- `debug_pairs_v3.py` — pair-by-pair B2 simulation, v4 vs v5 with RP-04 correction
- `debug_b1_v5.py` — full B1 simulation across 31 gradable products
- `worked_numbers.py` — step-by-step weight derivation for §3.3 and §4.3

---

## 8. Implementation Handoff Notes (for Data Agent)

1. **Do not touch `score_engine.py` or `signal_extractor.py` until D7 co-sign is obtained.** This is a D6 proposal.

2. The formula in §6 replaces `compute_component_b_score()` in `matrix_signal_probe_v4.py`. The Data Agent should create `matrix_signal_probe_v5.py` using the v4 reading layer (`structured_ingredient_reader.py` + `extract_all_markers_v4()`) unchanged, with only `compute_component_b_score_v5()` as the new formula.

3. The gold-set JSON (`matrix_gold_set_v1.json`) must be updated before running the v5 probe: swap RP-04's `higher` and `lower` barcodes. The `reason` should be updated to: `"oats 39% direct product-weight > oats 43%×65%=28% effective product-weight"`. The file is currently marked LOCKED; the Data Agent should note this as a Nutrition Agent-authorized correction with the governance basis in this document.

4. The v5 probe must re-run Gates B1, B2, B3 against the corrected gold set and emit a new report and results JSON.

5. The simulation in §7 used the exact v4 marker extractions as input — if the reader has changed between v4 and v5 implementation, re-run the full pipeline. The simulation result is the prediction; the gate report from the actual probe is the truth.

---

## 9. D7 Co-Sign Requirement

This is a scoring-behavior change that will affect ranking of products in live categories once promoted to the production engine. It requires Product Agent co-sign before Data Agent implements it. Two specific changes require co-sign:

1. **Grain-context non-grain penalty (0.5x)**: reduces the contribution of nuts/seeds/dried fruit to the whole-food signal in grain-context products. This may lower scores for products whose whole-food markers are predominantly non-grain (e.g. a product whose only whole-food marker is olive oil or tahini, in a product that also contains a small amount of oats). Impact: directionally correct but requires Product review of any product where this shift moves a grade boundary.

2. **Anchor nudge 0.15 -> 0.05**: increases score separation in the mixed band, reducing score compression around 52.5. This will make more mixed products distinguishable from each other. Impact: no product should move above or below its current tier (T1 or T2 products are anchor-independent once their raw dom_ratio is above 0.55 or below 0.35); the effect is confined to the T3 mixed band.

Neither change affects T1 or T2 gate passage at the population level (B1 holds at 96.8%). Neither adds a new hard chain or binary cap. Both are continuous and preserve the inversion invariant (adding refined weight cannot raise the score).

---

## 10. What This Spec Does Not Address

1. **Composite without parent_pct (barcode 7290106571945)**: the remaining B1 failure is a composite-parsing gap where `sub_stated_pct` cannot be used as effective product-weight because parent_pct is absent. This requires a separate design rule: when a parent composite has no stated_pct but its sub-ingredients have product-weight percentages (inferrable from context), use the sub-percentages directly. This is a distinct problem — not blocking the v5 formula promotion.

2. **Gold-set expansion**: the current 12 pairs adequately test the B2 gate at 95% bar. Adding more pairs is a future quality improvement, not a v5 prerequisite.

3. **Production engine wiring**: the formula prototype runs in `matrix_signal_probe_v5.py`; wiring into `score_engine.py` is deferred until D7 co-sign and a successful v5 probe run.

---

## v3.1 — NC-2 Addendum: Trace-Grain Guard + Sourdough Starter Classification
**Authored by:** Nutrition Agent (D6)
**Date:** 2026-06-25
**Trigger:** NC-2 regression check from D7 co-sign (`d7_cosign_v5_formula.md` Ruling 3)
**Status:** D6 RULING — requires Product Agent NC-2 close confirmation before Data Agent implementation

---

### A. The Flaw the NC-2 Check Exposed

The v5 M-2 rule fires the grain-context 0.5x penalty on any product where at least one grain whole marker is present. The NC-2 check found two products where this trigger condition is too coarse:

**7290107947480 (חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים — cereal chocolate bar):**

Label: `פתיתי דגנים 32% (אורז 26%, סוכר לבן, קמח תירס 2%, חיטה מלאה-גלוטן 1%, ...) ... שברי אגוזים 10.2% (שקדים, לוז)`

The whole-wheat sub-ingredient reads at 1% of product weight (position 4 within a 32% sub-composite that also contains rice 26%, sugar, and corn flour). The grain-context flag fires on this 1% whole-wheat trace. It then halves the nuts at 10.2% (almonds + hazelnuts), which are the actual dominant whole-food feature of the product. Score drops from 35.1 (D) to 27.6 (F) — a grade boundary crossing.

The nutritional reality: this product's whole-food character is nut-forward. The 1% whole wheat is a label-trace inside a heavily refined cereal composite; it does not confer grain density on the product. Penalizing the nuts because of a 1% whole-wheat trace is penalizing the product's genuine whole-food feature on the basis of an ingredient that is nutritionally invisible at that mass.

**481180 (לחם מחמצת שאור — sourdough bread):**

Label: `קמח חיטה לבן (75% מהקמח, 40% מהלחם) ... מחמצת חיטה לבן 18% (קמח חיטה לבן, מים) ... קמח חיטה מלא (25% מסך הקמחים, 15% מהלחם) ...`

Whole wheat flour is at 15% effective product weight. Sourdough starter appears as a named ingredient at 18% effective weight and was classified as a "non-grain whole marker" in the v5 NON_GRAIN_WHOLE_LABELS set. The grain-context fires on the 15% whole-wheat flour (legitimate), then halves the sourdough starter's 18% effective weight. Score drops from 38.0 (D) to 32.4 (F).

This is a double flaw: (1) sourdough starter should not be in NON_GRAIN_WHOLE_LABELS at all, for reasons ruled below; and (2) even if it were, an 18% starter in a bread with 15% whole-wheat flour is not a "non-grain whole dominates grain whole" situation — the starter mass here does not represent a whole-food nutritional contribution orthogonal to grain.

---

### B. Decision 1 — Trace-Grain Guard

#### B.1 The rule

The grain-context 0.5x penalty shall apply only when grain whole markers represent a MEANINGFUL share of the product's scored ingredient mass, defined as:

**Activation condition (both required):**
1. **Absolute floor:** grain whole effective weight >= 5% of product weight
2. **Relative floor:** grain whole effective weight >= 50% of non-grain whole effective weight (before the penalty is applied)

Either condition failing independently is not sufficient grounds to activate the penalty. Both must hold simultaneously. If either fails, the grain-context flag is not set and all markers score at full weight.

#### B.2 Nutritional justification for the thresholds

**5% absolute floor:**

5% of product weight is the minimum level at which a grain ingredient contributes meaningfully to the product's grain-starch matrix character. Below this level, a grain ingredient is present for technical or labelling reasons (regulatory clean-label gestures, minor functional additions) rather than as a structural matrix contributor.

The corpus supports 5% as a defensible floor. In the current test set, the 10 T1 products (whole-grain dominant) have grain whole effective weights ranging from 15% to 95%. The 14 T2 products (refined dominant) have grain whole effective weights at 0% or below 3% (where present at all). The 1% whole-wheat trace in 7290107947480 is 5x below this floor. A 5% threshold correctly excludes it and correctly includes all genuine T1 and T2 products.

This is not calibrated to make 7290107947480 pass — it is calibrated to exclude ingredients that constitute less than one-in-twenty grams of the product from triggering a structural product-class determination. An ingredient at 1% of product weight is nutritionally immaterial as a matrix driver regardless of its class.

**50% relative floor:**

The relative floor addresses products where grain whole is present at a meaningful absolute level but is still substantially dominated by non-grain whole markers. The penalty's intent is to correct for non-grain whole markers inflating the grain-density signal. That correction is only justified when grain whole is actually the primary whole-food source, or at least co-equal with it. If non-grain whole effective weight is more than twice the grain whole effective weight before the penalty, the formula is penalizing the dominant feature on behalf of a minority feature — an inversion of the signal's logic.

The D7 co-sign Ruling 3 states this directly: "there is a class of products where the penalty could produce an indefensible drop: a product that is genuinely nut- or seed-forward... the grain context triggers on the trace oat presence, and the 0.5x penalty then halves the weight of what is actually the dominant whole-food feature." The relative floor operationalizes that concern as a precise, label-derivable rule.

**Evidence tier: Moderate.** The thresholds are grounded in corpus behavior and nutritional rationale, not a controlled trial. The 5% floor is a defensible minimum-materiality threshold consistent with how food science treats ingredient-level contributions to product matrix character. The 50% relative floor is a principled symmetry condition: the penalty only fires when grain whole is at least as large as what it is penalizing.

#### B.3 Effect on 7290107947480

Before guard: grain_whole_w = 0.0690 (1% whole wheat inside the cereal sub-composite), non_grain_whole_w (before penalty) = 0.2067 (nuts 10.2%).

Guard check:
- Absolute: 6.9% < 5%? NO — 6.9% passes the absolute floor.

Wait — the v5 report states grain_whole_w = 0.0690, which is 6.9% of product weight. This is above 5%.

Let me re-examine this carefully. The label states `חיטה מלאה-גלוטן 1%` as a sub-ingredient of `פתיתי דגנים 32%`. The grain_whole_w = 0.0690 is the effective weight as computed by the formula — but 1% whole wheat inside a 32% composite gives effective_pct = 1% × 32%? No — the v5 report description says "1% whole wheat in flakes" (RP-05 reason). The reader interprets the `1%` as a sub-ingredient percentage. If it means 1% of the 32% composite, effective product weight = 0.01 × 0.32 = 0.0032 = 0.32%. If it means 1% of product weight stated directly, effective weight = 1%.

The v5 NC-2 entry reads: `grain_whole_w=0.0690`. The ingredient list states the sub-composite `פתיתי דגנים 32%` and within it `חיטה מלאה-גלוטן 1%`. The reader's interpretation of this sub-pct matters for the guard threshold.

Looking at the RP-05 pair reason: "1% whole wheat in flakes" — this product appears as the LOWER product in RP-05 (43% whole oat product vs 1%-grain bar), and in RP-10 (35% whole wheat vs 1%-grain bar). Both pairs treat it correctly as a low-grain product. The grain_whole_w = 0.0690 likely reflects the reader computing 1% × some parent context, or the reader treating the 1% as direct product-weight within the sub-composite.

At either interpretation (0.32% if properly nested, or 6.9% if the reader inflates via position-weight), the nutritional conclusion is identical: a sub-ingredient of a cereal flake composite that is itself at most 1% of the composite does not confer grain-density. The absolute floor of 5% must be evaluated against the ingredient's true product-weight fraction.

**Refined rule for the absolute floor:** the grain_whole_w used to evaluate the 5% absolute floor must be computed using the strict effective_pct (stated_pct for sub-composites multiplied through the parent), not the position-weight fallback. Where a parent composite has a stated_pct and the sub-ingredient has a stated_pct expressed as a fraction of the composite, the product-weight contribution is parent_stated_pct × sub_stated_pct. For 7290107947480: parent = 32%, sub = 1% → effective product-weight = 0.32%. This falls far below the 5% floor, and the grain-context flag does not activate.

Even if the reader currently computes grain_whole_w = 0.0690 (6.9%) via a different path (e.g., treating the 1% as direct product-weight or position-distributing within the composite), the correct value from the label is 0.32%. The guard must be computed on label-correct effective weight. Data Agent must verify the reader's effective_pct computation for nested sub-ingredients with stated percentages.

**Guard result for 7290107947480:** grain whole effective product-weight = 0.32% (label-correct) or at most 1% if treated as direct product-weight. Both are below the 5% absolute floor. Grain-context flag does NOT activate. Nuts at 10.2% score at full weight. Score reverts toward v4 value (35.1, D). Grade boundary crossing is eliminated.

**Effect on RP-05 and RP-10 pairs:** both pairs correctly have 7290107947480 as the LOWER product. With the guard preventing the grain-context from firing on this bar, its score increases back toward ~35 (D). Both pairs have higher products at 75.7 and 39.8 respectively — margins of +40 and +4.7 points. Neither pair is threatened by the guard restoring the bar's score. Both pairs continue to pass.

#### B.4 Corpus-wide re-validation requirement

The guard introduces a new code path (the two-condition activation check). Data Agent must:
1. Run the guard against all scored products in the gold set v2 (67 products) and verify:
   - No T1 product (genuine whole-grain dominant) has its grain-context flag suppressed by the guard.
   - No currently-passing B2 pair changes direction.
2. Emit the activation/suppression table: for each product, whether the guard was active, suppressed, or not applicable (no non-grain whole markers present).

This is a re-validation step, not a full re-gate. The B1, B2, B3 gate results from v5 remain the baseline; the guard must not degrade any of them. If any T1 product loses its grain-context flag (meaning the guard incorrectly suppresses a genuine grain-dense product), the absolute floor must be reviewed — it is set too high.

---

### C. Decision 2 — Sourdough Starter Classification

#### C.1 Ruling

**Sourdough starter (`sourdough_starter`) must be removed from `NON_GRAIN_WHOLE_LABELS` entirely.** It is not a whole-food contributor of the class the signal is designed to measure. Its presence in that list is a classification error introduced when the marker lexicon was assembled.

#### C.2 Nutritional basis

The matrix signal's `NON_GRAIN_WHOLE_LABELS` set contains ingredients that are genuine whole-food contributors on a nutritional axis orthogonal to grain density: nuts (fat, protein, minerals), seeds (fat, micronutrients), dried fruit (fiber, concentrated sugars), tahini (fat, protein from sesame), olive oil (monounsaturated fat).

Sourdough starter is none of these things. It is a live fermentation culture — flour, water, and microbial communities (Lactobacillaceae, wild yeasts). Its nutritional contributions are:
- Organic acid production (lactic and acetic acids), which modifies bread pH and texture
- Partial phytate hydrolysis, improving mineral bioaccessibility in the final product
- CO2 and alcohol production as leavening byproducts (both leave the crumb)
- A small residual microbial mass (largely inactivated by baking)

Critically: sourdough starter contributes no significant independent whole-food mass in the nutritional sense. Its flour base is refined wheat flour (as confirmed by the 481180 label: `מחמצת חיטה לבן — white wheat sourdough`). It is classified as a leavening and fermentation agent. When a bread label lists `מחמצת 18%`, those 18 grams per 100g of bread are predominantly water and flour — the same flour the bread is already made from. The starter does not introduce new whole-food nutrients; it modifies the matrix of existing ingredients.

**This is why sourdough starter should not be in either list.** It is not a non-grain whole marker (it adds no independent nutritional whole-food mass). It is also not a grain whole marker (it is a process ingredient, not a structural whole-grain contributor). The correct classification is: neutral / process ingredient. It should not participate in whole-vs-refined scoring at all.

Assigning starter to NON_GRAIN_WHOLE_LABELS and then applying the grain-context penalty was therefore double-wrong: it treated a process ingredient as a nutritional whole-food contributor, and then penalized it for not being grain. The effect was to penalize a bread for using traditional fermentation — which is opposite to Bari's fermentation-quality philosophy (genuine fermentation is a positive signal, not a penalized one).

**Evidence tier: Strong for the neutrality ruling.** Sourdough starter's composition (flour + water + microbial communities) is uncontested food science. Its nutritional profile is well-characterized. The ruling that it is a process ingredient rather than a whole-food contributor is a direct application of ingredient classification, not an inference. The phytate reduction benefit of sourdough fermentation is real (evidence tier: Moderate from in-vitro bioaccessibility literature, per KB-003) but that benefit accrues to the bread's mineral bioaccessibility, not to the starter's mass contribution — it is a process effect, captured separately if Bari chooses to score fermentation quality.

#### C.3 Correct classification in the signal

Remove `sourdough_starter` from `NON_GRAIN_WHOLE_LABELS`. Do not add it to `GRAIN_WHOLE_LABELS`. It should receive no classification in either set — it is invisible to the matrix signal. Any effective_pct associated with sourdough starter is not added to the whole_weight or refined_weight computation.

This is consistent with the existing treatment of water, salt, and other process ingredients, which are also unclassified and therefore invisible to the signal.

#### C.4 Effect on 481180

Before fix: sourdough_starter at 18% effective weight fires as NON_GRAIN_WHOLE, grain-context fires on whole_wheat_flour at 15%, starter gets 0.5x penalty → starter contributes 9% to whole_weight.

After fix: sourdough_starter is unclassified. It does not enter either whole_weight or refined_weight. The marker set for 481180 becomes:
- whole: whole_wheat_flour at 15% (grain whole — direct label statement: "25% מסך הקמחים, 15% מהלחם")
- refined: refined_wheat_flour at 40% (direct label statement: "75% מהקמח, 40% מהלחם")
- unclassified: sourdough starter (18%), water, salt, gluten, preservative

grain_whole_w = 0.150, refined_w = 0.400, total_marked = 0.550
dominance_ratio = 0.150 / 0.550 = 0.273

anchor: highest-weight marker is refined_wheat_flour (0.40) — refined anchor. raw dom_ratio 0.273 > 0.5? No. Refined anchor nudge applies only if dom_ratio > 0.5 (to push down). Here dom_ratio = 0.273, anchor is refined, nudge does not push further (already below 0.5 — the anchor is correctly specified to only nudge toward 0.5 from below for whole, or from above for refined, not through it). Score = 10 + 0.273 × 85 = 33.2.

This is approximately the v4 score (38.0) minus the sourdough removal effect. The product scores as D — which is the nutritionally honest result for a bread that is 40% white flour, 15% whole wheat, and 18% starter (also white-flour based). The D→F regression caused by the v5 misclassification is eliminated. The score lands in the low-D range, which accurately represents: this is mostly white bread with a meaningful but minority whole-wheat component and genuine sourdough fermentation.

Note: the score (approximately 33) is below the v4 score (38.0) because removing sourdough from the whole-weight pool correctly reduces the total whole_weight. The v4 score of 38.0 was itself inflated by counting sourdough starter as a whole-food contributor. The correction is directionally right even if the final score differs from v4. This is not a regression — it is a correction of two compounded errors.

**Grade outcome:** score ~33 remains D. No grade boundary crossing from v4 (D) to v5-corrected (D). The NC-2 flag is resolved.

#### C.5 Effect on existing fermentation signals

Removing sourdough_starter from NON_GRAIN_WHOLE_LABELS does not affect any existing fermentation quality signal. Bari's fermentation scoring (genuine vs industrial vs theater) is handled separately from the matrix signal. This change makes the matrix signal silent on fermentation agents — it does not penalize or reward them. That is the correct behavior: fermentation quality is scored on its own axis.

Data Agent must confirm no other lexicon entry currently acts as a sourdough proxy (e.g., `sourdough_starter_rye`, `levain`, or similar Hebrew-text patterns) — any such entry should receive the same neutral classification.

---

### D. D7 Co-Sign Requirement for This Addendum

The v5 formula was co-signed by Product Agent with NC-2 as an explicit condition: "flag [grade-boundary movers] for Nutrition re-review before the formula is promoted to production." This addendum provides that re-review and proposes two refinements:

1. **Trace-grain guard** (absolute 5% + relative 50% activation condition for grain-context flag)
2. **Sourdough starter reclassification** (removed from NON_GRAIN_WHOLE_LABELS, classified as neutral/process ingredient)

Both changes modify the M-2 rule that Product already co-signed. The question is whether they require a fresh full D7 co-sign or whether Product's confirmation that NC-2 is closed is sufficient.

**My ruling:** Product's confirmation that NC-2 is closed is sufficient — no fresh full D7 co-sign is required. The reasoning:

The D7 co-sign on v5 was given WITH NC-2 as a condition precisely because this re-review was anticipated. Product authorized the penalty with the explicit expectation that Nutrition would examine grade-boundary movers and refine the rule. This addendum is the fulfillment of that condition, not a new proposal outside the co-signed scope.

The two refinements are narrowing changes that move scores toward v4 values (they remove over-penalties, not add new penalties). They do not introduce new chains, new hard caps, or new binary triggers. The monotonicity invariant is preserved: neither refinement can cause a score to rise by adding refined ingredients or removing whole ingredients. The inversion-invariant guardrail is intact.

If Product identifies a concern with either refinement that it considers outside the scope of NC-2 closure — particularly if the relative floor (50%) appears to shelter products that genuinely have grain-context activated — Product should escalate to a fresh D7 co-sign. Absent such a concern, this addendum proceeds as NC-2 closure.

**Action required from Product Agent:** confirm NC-2 is closed (or flag if fresh D7 co-sign is needed). Data Agent must not implement until Product has confirmed.

---

### E. Summary of Refined M-2 Rule (Implementable Spec Delta)

The following replaces the `has_grain_whole` determination in §6's pseudocode:

```python
# Classification sets — unchanged from v5
GRAIN_WHOLE_LABELS = { ... }  # unchanged
NON_GRAIN_WHOLE_LABELS = {
    "nuts", "almonds", "peanuts", "pistachios", "cashews",
    "seeds_specific", "seeds_generic", "sesame_seeds",
    "chia_seeds", "flax_seeds",
    "dates", "raisins",
    "tahini", "olive_oil", "butter_dairy",
    # "sourdough_starter" REMOVED — reclassified as neutral/process ingredient
}

# v3.1 guard: grain-context requires meaningful grain presence
GRAIN_CONTEXT_ABS_FLOOR = 0.05   # grain whole effective weight >= 5% of product weight
GRAIN_CONTEXT_REL_FLOOR = 0.50   # grain whole effective weight >= 50% of non-grain whole
                                   # effective weight (before any penalty)

def has_meaningful_grain_context(markers: list[dict], effective_weight_fn) -> bool:
    """
    True only when grain whole markers are a meaningful share of the product.
    Both conditions must hold simultaneously.
    Effective weight used here is pre-penalty (base weight, before M-2 discount).
    """
    grain_whole_ew = sum(
        effective_weight_fn(m, apply_grain_penalty=False)
        for m in markers
        if m["class"] == "whole" and m["label"] in GRAIN_WHOLE_LABELS
    )
    non_grain_whole_ew = sum(
        effective_weight_fn(m, apply_grain_penalty=False)
        for m in markers
        if m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE_LABELS
    )

    abs_condition = grain_whole_ew >= GRAIN_CONTEXT_ABS_FLOOR
    rel_condition = (non_grain_whole_ew == 0.0
                     or grain_whole_ew >= GRAIN_CONTEXT_REL_FLOOR * non_grain_whole_ew)

    return abs_condition and rel_condition

# Replace the v5 has_grain_whole boolean with:
has_grain_context = has_meaningful_grain_context(markers, effective_weight)
# Then use has_grain_context everywhere v5 used has_grain_whole
```

**Critical implementation note on effective_pct for nested sub-ingredients:**

The grain_whole_ew computation in `has_meaningful_grain_context` must use label-correct effective_pct, not position-weight fallback, for sub-ingredients of a stated composite. If a grain whole marker has a stated_pct that was declared as a percentage of a parent composite (and the parent also has a stated_pct), the effective product-weight is `parent_stated_pct * sub_stated_pct / 100`. Data Agent must verify the reader uses this multiplication for 7290107947480's `חיטה מלאה 1%` within `פתיתי דגנים 32%` and does not fall back to position-weight for this sub-ingredient.

---

### F. Re-Validation Scope (for Data Agent after Product confirms NC-2 close)

1. Apply the refined M-2 rule (trace-grain guard + sourdough reclassification) to `matrix_signal_probe_v5.py` to produce `matrix_signal_probe_v5_1.py`.
2. Run against the same gold set v2 (67 products, 20 T3 pairs).
3. Confirm:
   - B1 >= 90% (baseline: 30/31 = 96.8%)
   - B2 >= 95% (baseline: 19/20 = 95.0%, with RP-04 still the known annotation issue)
   - B3 = 100% (reading layer unchanged)
4. Emit the grain-context activation table: for each product, does `has_meaningful_grain_context` return True or False, and why (which condition failed if False).
5. Confirm `sourdough_starter` (and any synonyms/variants) scores 0 in whole_weight for all bread products in the corpus.
6. Confirm 7290107947480's score reverts to approximately the v4 range (D, not F).
7. Confirm 481180's score is approximately 33 (D, not F).

Independent QA re-grades after Data Agent run. Nutrition Agent does not self-certify.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v3.md",
      "action": "created",
      "sha256": "7AB11760CF3D84120A52118ADA8E5F8BAE4C388373464BECBB21C67B7868A8BD"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/debug_pairs.py",
      "action": "created",
      "sha256": "7F0096E49AB829BC29DF6FC954329C4837255365469128045D3B8DCF40BE3697"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/debug_pairs_v2.py",
      "action": "created",
      "sha256": "3125D95EAA61AB9A837EFA898422993B5F6D0411A445C150A1B8A4AF48072A52"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/debug_pairs_v3.py",
      "action": "created",
      "sha256": "21ECE6E8666F32BD1284C8EFC351A5BB596238A7D05010034CA0AE79D96A658B"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/debug_b1_v5.py",
      "action": "created",
      "sha256": "D061C8C92A6769615B469DF00FE7CC5D4F8CCEF56E730AD6630375DF7FF8D887"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/worked_numbers.py",
      "action": "created",
      "sha256": "BC720FCC5508FAD562231DD2C669D2B4638D11176901CC9BB618EFD155CBF4F9"
    }
  ],
  "counts": {
    "b2_pairs_passing_v4": "9/12 (from matrix_signal_probe_v4_results.json gate_B2.pass_count)",
    "b2_pairs_passing_v5_with_rp04_correction": "12/12 (from debug_pairs_v3.py — all 12 pairs pass)",
    "b1_passing_v5": "30/31 = 96.8% (from debug_b1_v5.py — same as v4, no regression)",
    "b3_coverage_unchanged": "55/55 = 100.0% (reading layer unchanged)",
    "failing_pairs_fixed": "3/3 (RP-03, RP-04 corrected, RP-08 — all now pass)",
    "gold_set_corrections": "1/12 pairs (RP-04 direction inverted — nutritional ruling in §5)",
    "formula_changes": "2 (grain-context 0.5x penalty + anchor nudge 0.15->0.05)"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/shared_reader_build_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v4.py", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v2.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v4_results.json", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md", "exit_code": 0},
    {"cmd": "python debug_pairs.py (weight decomposition for 3 failing pairs)", "exit_code": 0},
    {"cmd": "python debug_pairs_v2.py (dead-zone analysis + v5 candidate formulas)", "exit_code": 0},
    {"cmd": "python debug_pairs_v3.py (full B2 gate simulation v4 vs v5, 12 pairs)", "exit_code": 0},
    {"cmd": "python debug_b1_v5.py (B1 gate simulation v5, 31 products)", "exit_code": 0},
    {"cmd": "python worked_numbers.py (step-by-step derivation for spec §3.3 and §4.3)", "exit_code": 0}
  ],
  "not_done": [
    "matrix_signal_probe_v5.py not yet created — Data Agent implements after D7 co-sign",
    "matrix_gold_set_v1.json RP-04 correction not yet applied — Data Agent applies before v5 probe run",
    "D7 Product Agent co-sign not yet obtained — required before Data Agent implementation",
    "Production engine (score_engine.py / signal_extractor.py) not modified — deferred until D7",
    "Composite-without-parent-pct design gap (barcode 7290106571945, B1 failure) not addressed in this addendum — separate design task",
    "debug_pairs*.py and worked_numbers.py are validation scripts, not production code — Data Agent should delete them after v5 probe is committed"
  ],
  "self_check": "Acceptance test: Data Agent runs matrix_signal_probe_v5.py on the corrected gold set and reports B1>=90%, B2>=95%, B3>=95%. Simulated result from debug_pairs_v3.py + debug_b1_v5.py: B1=96.8% [30/31], B2=100.0% [12/12], B3=100.0% [55/55]. All three gates clear. Simulation used exact v4 marker extractions; actual probe may differ slightly if reader state differs."
}
```

---

### v3.1 Return Contract (NC-2 Addendum — D6 only)

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v3.md",
      "action": "modified",
      "sha256": "SELF-REFERENTIAL — orchestrator runs Get-FileHash after acceptance"
    }
  ],
  "counts": {
    "nc2_grade_boundary_movers": "2/2 reviewed (7290107947480 D->F, 481180 D->F — source: shared_reader_build_v1.md v5 NC-2 section)",
    "nc2_refinements_proposed": "2 (trace-grain guard; sourdough starter reclassification — source: this addendum §B and §C)",
    "grain_context_abs_floor": "5% of product weight (label-correct effective_pct for nested composites)",
    "grain_context_rel_floor": "50% — grain whole must be >= 50% of non-grain whole effective weight (pre-penalty)",
    "sourdough_starter_labels_removed": "1 label removed from NON_GRAIN_WHOLE_LABELS (source: §C.3)",
    "expected_score_7290107947480": "approximately v4 range (~35, D) after guard prevents grain-context activation (source: §B.3 analysis; label effective_pct 0.32% < 5% floor)",
    "expected_score_481180": "approximately 33 (D) after sourdough reclassification (source: §C.4 worked calculation)",
    "nc2_d7_requirement": "Product Agent NC-2 close confirmation (not fresh full D7 co-sign) — basis: §D ruling"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/shared_reader_build_v1.md (v5 NC-2 section)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v3.md (v5 formula + worked numbers)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/d7_cosign_v5_formula.md (Ruling 3, NC-2 condition)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v5_results.json (NC-2 entries, pair results)", "exit_code": 0},
    {"cmd": "Grep 7290107947480|481180 in matrix_gold_set_v2.json (label ingredient text verification)", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "Data Agent implementation of trace-grain guard and sourdough reclassification in matrix_signal_probe_v5_1.py — deferred until Product Agent confirms NC-2 closed",
    "Re-validation run (v5_1 probe) against gold set v2 — deferred until Product confirmation",
    "Grain-context activation table across full 67-product gold set — Data Agent action post-confirmation",
    "Verification that reader correctly multiplies nested sub-ingredient stated_pct through parent for 7290107947480 — Data Agent must confirm before running v5_1",
    "Production engine wiring (score_engine.py / signal_extractor.py) — deferred until all gate conditions satisfied (unchanged from v3.0)"
  ],
  "self_check": "Acceptance test for this addendum: Data Agent runs matrix_signal_probe_v5_1.py, emits grain-context activation table, and reports (1) 7290107947480 grain-context flag = False, score in D range; (2) 481180 sourdough_starter contribution to whole_weight = 0, score approximately 33 (D); (3) B1 >= 90%, B2 >= 95%, B3 = 100%; (4) no T1 product has grain-context suppressed by the guard. Nutrition Agent does not self-certify — Independent QA re-grades."
}
```
