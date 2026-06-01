# BSIP2-061 Water-to-Primary Ingredient Predominance — Pilot Design

**Signal:** BSIP2-061
**Document:** bsip2_061_water_predominance_pilot.md
**Owner:** Chief Nutrition Officer
**Status:** PILOT DESIGN — No scoring changes. No implementation.
**Created:** 2026-05-31
**Task:** TASK-048
**Governance reference:** bsip2_signal_governance_v1.md — Section 3 (BSIP2-061 routing matrix)

---

## Signal Statement

Water-to-Primary Ingredient Predominance detects whether water appears before the dominant functional ingredient in a product's ingredient list. Under Israeli food labeling law, ingredients are listed in descending order by weight. When water precedes chickpeas in a hummus product, or sesame in a tahini product, it signals that the product's functional content has been diluted to the point where water — a zero-nutritional-value ingredient — constitutes the largest single component by weight.

This is a structural proxy for reconstruction. A well-made hummus does not need water to be its primary ingredient. Chickpeas and tahini together provide sufficient liquid from natural moisture. When water leads the list, the chickpea or tahini proportion has been reduced below the threshold where it can define the product's physical structure.

---

## Section 1 — Signal Logic

### 1.1 Core Detection Mechanism

The signal detects ingredient list position of water relative to the product's primary functional ingredient.

**Trigger condition:**
- Water (`מים`, `מי`, `water`) appears at position 1 or 2 in the ingredients list
- AND the primary functional ingredient (chickpeas, sesame, nut, dairy base) appears at position 3 or later

**Non-trigger (signal suppressed):**
- Water appears after the primary functional ingredient at any position
- Ingredient list is absent or insufficient for position detection (signal returns `not_evaluable`)
- Product is routed to an exclusion category (Section 3)

### 1.2 Primary Functional Ingredient by Category

The signal requires knowing what "primary functional ingredient" means per category. Without this anchor, water's position is uninterpretable.

| Category | Primary Functional Ingredient | Hebrew Detection Terms |
|----------|------------------------------|----------------------|
| Hummus | Cooked chickpeas | חומוס, גרגירי חומוס, חומוס מבושל, chickpeas |
| Tahini-based dips | Sesame / raw tahini | טחינה גולמית, טחינה, שומשום |
| Nut butters | Named nut or seed | בוטנים, שקדים, קשיו, גרעיני דלעת |
| Dairy spreads | Milk or cream | שמנת, גבינה, קוטג', יוגורט, חלב |
| Dense sauces and dips | Named primary vegetable or legume | עגבניות, פלפל, חצילים, סלק, גזר |

### 1.3 Signal Output

The signal produces three states:

| State | Condition | Scoring Effect |
|-------|-----------|----------------|
| `WATER_PREDOMINANT` | Water at position 1 or 2, functional ingredient at position 3+ | Full penalty applied |
| `WATER_EARLY` | Water at position 1 or 2, functional ingredient also at position 1 or 2 | Half penalty applied (borderline case) |
| `NOT_PREDOMINANT` | Water absent from positions 1–2, or absent entirely | No effect |
| `NOT_EVALUABLE` | No ingredient list, category exclusion, or primary ingredient undetectable | Signal suppressed |

---

## Section 2 — Activation Categories

### 2.1 Categories Where Signal Activates

**Hummus**
- Water is not structurally necessary as a first ingredient in any authentic hummus. Cooked chickpeas and raw tahini provide natural moisture. Water in the first position is a reliable dilution signal.
- Expected firing rate in hummus corpus: unknown (pilot measurement objective). Estimated 15–30% of products based on known reconstructed archetypes.

**Tahini and tahini-based dips**
- Raw tahini (טחינה גולמית) is composed entirely of sesame. Water should not precede sesame as a primary ingredient. Water-first tahini products are structurally thinned.
- Not currently in corpus. Relevant for future pilot extension.

**Nut butters**
- Peanut butter, almond butter, and seed butters should be nut/seed dominant. Water-first nut butter is structurally reconstituted.
- Not currently in corpus.

**Dairy spreads**
- Labaneh, cream cheese spreads, soft cheese spreads. Milk protein or cream should dominate. Water before dairy base signals a thinned product.
- Not currently in corpus. Relevant for dairy category launch.

**Dense sauces and dips (sauce_spread archetype)**
- Vegetable-based dips with a named primary vegetable as the dominant structural ingredient (eggplant dip, roasted pepper dip, beet spread). Water before the named vegetable signals dilution.
- In-scope for pilot — these are part of the hummus corpus (routed to sauce_spread).
- **Critical nuance:** many vegetable spreads naturally contain no added water because the vegetables themselves provide all liquid. In these products the signal returns `NOT_PREDOMINANT` by default.

### 2.2 Activation Summary Table

| Category | Activates | Rationale |
|----------|-----------|-----------|
| Hummus | YES | Water before chickpeas is a dilution signal |
| Tahini-based dips | YES | Water before sesame is a dilution signal |
| Nut butters | YES | Water before nuts is reconstruction |
| Dairy spreads | YES | Water before milk/cream is thinning |
| Dense vegetable dips | YES | Water before primary vegetable is dilution |
| Dense sauces (paste-based) | YES | Water before primary ingredient signals thinning |
| Light vinaigrette sauces | NO | Water/vinegar are the archetype base — not dilution |
| Hot sauces (liquid category) | NO | Liquid by archetype — water is structural |

---

## Section 3 — Exclusion Rules

### 3.1 Hard Exclusions (Signal Does Not Fire)

**Beverages**
- Water is the category-defining matrix. Water appearing at position 1 is the expected and correct formulation for any beverage. The signal is category-meaningless here.
- Routing gate: any product with `archetype = beverage` → signal suppressed.

**Soups**
- Broth and water are the structural base for any soup. Water at position 1 is architecturally correct.
- Routing gate: any product with `archetype = soup` → signal suppressed.

**Fruit purees and fruit spreads**
- Whole fruit contains 80–93% water by weight. When whole fruit is cooked or processed into a spread, some water is released as a processing artifact. If water appears in the ingredient list separately from the fruit, it may be process water (released during cooking) rather than a deliberate dilution addition. The distinction is not resolvable from the ingredient list alone.
- Furthermore, BSIP2-063 (Fruit Matrix Quality) is designed to evaluate quality in this category specifically. Two signals should not cover the same territory with different logic.
- Routing gate: any product routed to fruit-matrix category → signal suppressed.

**Bread and grain-based products**
- Water is a structural ingredient in bread making (hydrates gluten, activates leavening). Water before flour is the normal and expected formulation for all bread products. Its position has no dilution interpretation in this context.
- Routing gate: any product with `archetype = bread` → signal suppressed.

**Cereals and extruded grain products**
- Water is added during grain processing (steam, extrusion, puffing). Its presence in the ingredient list is a process artifact, not a formulation quality indicator.
- Routing gate: any product with `archetype = cereal_system` → signal suppressed.

**Naturally high-water vegetables and condiments**
- Fresh salsa, gazpacho, pico de gallo — products whose primary ingredients (tomatoes, peppers, cucumbers) are naturally >90% water. In these products, water may not appear in the ingredient list at all (because it comes from the vegetables themselves), or it may appear as a minor addition. The signal is structurally inapplicable here.
- Resolution: if the product's primary functional ingredient is a naturally high-water vegetable (tomato, cucumber, pepper) AND no added water is listed, signal returns `NOT_EVALUABLE`. If water is listed AND precedes the primary vegetable, treat as borderline (`WATER_EARLY`) — do not fire full penalty.

**Matbucha (cooked tomato-pepper spread)**
- Matbucha is a special case within the sauce_spread archetype. Its natural composition is cooked tomatoes + peppers + oil + spices. Tomatoes are ~93% water. Water released during cooking is a natural processing artifact, not a quality-degrading addition.
- If matbucha products list `מים` (water) before tomatoes, this requires manual review before the signal is used as a scoring input for this sub-category. Flag for human review during pilot; do not score automatically.

### 3.2 Exclusion Decision Tree

```
Product enters BSIP2-061 evaluation
        │
        ▼
Is archetype one of: beverage, soup, bread, cereal_system?
        │
       YES → Signal suppressed (NOT_EVALUABLE)
        │
       NO ▼
Is product a fruit-matrix category?
        │
       YES → Signal suppressed (NOT_EVALUABLE) — defer to BSIP2-063
        │
       NO ▼
Is primary functional ingredient a naturally high-water vegetable (tomato, cucumber, pepper)?
        │
       YES → Is added water explicitly listed before the vegetable?
       │         │
       │        YES → Return WATER_EARLY (half penalty only)
       │         │
       │        NO → Return NOT_PREDOMINANT
        │
       NO ▼
Is ingredient list available and parseable?
        │
       NO → Return NOT_EVALUABLE
        │
       YES ▼
Does water appear at position 1 or 2?
        │
       NO → Return NOT_PREDOMINANT (no effect)
        │
       YES ▼
Does primary functional ingredient appear at position 3 or later?
        │
       YES → Return WATER_PREDOMINANT (full penalty)
        │
       NO → Return WATER_EARLY (half penalty)
```

---

## Section 4 — Scoring Proposal

### 4.1 Three Options

**Option A — No Score Impact (Detection flag only)**

The signal fires and is logged. It is visible in the product trace and available for transparency features, but produces no change to the final score.

- Advantages: zero baseline disruption; purely diagnostic; allows empirical data collection on firing rate and false positive rate before any scoring commitment
- Disadvantages: does not address any failure mode; does not improve scoring accuracy; creates a governance liability (signal exists but does nothing, eroding interpretability)
- Use case: appropriate only if the CNO requires an additional validation cycle before any score impact

**Option B — Low Impact (within whole_food_integrity dimension, max −4 pts to final score)**

The signal reduces the `whole_food_integrity` dimension score when `WATER_PREDOMINANT` is detected. Since `whole_food_integrity` carries 4% weight and a 0–100 score range, the maximum contribution to the final score is 4 points.

- Mechanism: reduce `whole_food_integrity` score by 40 points for `WATER_PREDOMINANT` (4% × 40 = 1.6 pts final); reduce by 20 points for `WATER_EARLY` (4% × 20 = 0.8 pts final). At maximum dimension compression: 4 pts.
- Advantages: self-contained within the smallest existing dimension; no new penalty layer; bounded; calibratable; interpretable ("whole food integrity was reduced because water precedes the primary ingredient")
- Disadvantages: modest final score impact may be insufficient to distinguish reconstructed products from well-made ones; limited discriminating power in the current corpus where scores cluster tightly (std dev 9.64)

**Option C — Medium Impact (post-cap penalty, max −10 pts to final score)**

The signal fires as a new post-cap penalty after all dimension scoring and hard caps.

- Mechanism: `WATER_PREDOMINANT` → −10 pts; `WATER_EARLY` → −5 pts. Applied after NOVA cap, additive cap, sodium cap. Stacks with existing post-cap penalties (seed oil, ingredient count, etc.).
- Advantages: meaningful discriminating power; likely to produce rank changes that surface correctly-penalised reconstructed products; aligns with the governance cap established in the framework (max −10 pts)
- Disadvantages: adds a new penalty layer to a stack that already has 4 existing penalties; compounds with SEED_OIL_PRESENT (fires on 43/69 hummus products, many of which are the same products likely to have water first); requires stacking cap validation to ensure the −20 total penalty ceiling holds

### 4.2 Recommendation — Option B (Low Impact, within whole_food_integrity)

**Recommended for pilot phase: Option B.**

Rationale:

1. **Baseline stability.** The hummus corpus has a std dev of 9.64 with a tight cluster (58% of products in the 60–70 band). A −10 pt penalty would move products across grade thresholds in ways that cannot be validated without empirical firing data. Option B's max −4 pt impact is bounded enough to measure without destabilising the baseline.

2. **Penalty stack discipline.** The SEED_OIL_PRESENT penalty already fires on 43/69 products. Many of the same products with water first will also have refined seed oils (they are both symptoms of the same reconstructed architecture). Adding a −10 pt penalty on top risks compounding to −13 pts (SEED_OIL + WATER_PREDOMINANT) for the same root cause. Option B is dimensionally contained and does not add to the penalty stack.

3. **Governance alignment.** The signal governance framework explicitly reserves Option C (post-cap penalty at max −10 pts) for production deployment after pilot validation. The pilot purpose is to measure, not to maximise impact.

4. **Interpretability.** "This product's whole food integrity score was reduced because water appears before chickpeas" is a clear, defensible explanation. A new penalty layer is harder to explain without triggering a CNO review of the full penalty stack.

**Option C is the correct production target.** If the pilot confirms that the signal fires with high directionality and low false positive rate, promotion to Option C is the recommended path. Option B is a stepping stone, not the end state.

---

## Section 5 — Expected Corpus Impact

### 5.1 Pilot Corpus

**Primary corpus for pilot:** run_hummus_002 — 69 products (Shufersal hummus and savory dips).

**Products with ingredient lists available:** approximately 50–55 of 69 (6 NOVA 1 products have no ingredient data; 2 insufficient_data products are excluded).

**Estimated firing rate:** 15–30% of products with ingredient lists. Reconstructed archetypes (Archetype X and Y from the review framework) are the primary targets. These are the products with "chickpea paste at low declared percentage, water or oil listed before chickpeas" — described as the bottom 10% of the corpus.

### 5.2 Expected Categories Affected

| Sub-category within corpus | Expected signal behaviour |
|---------------------------|--------------------------|
| Traditional 3–6 ingredient hummus (Archetypes A, B) | NOT_PREDOMINANT — signal does not fire; chickpeas listed first |
| Standard commercial hummus (6–10 ingredients) | Mixed — some will have water in position 2 or 3; expected 30–40% WATER_EARLY |
| Reconstructed hummus (Archetypes X, Y — 10–15 ingredients) | WATER_PREDOMINANT — signal fires; water before chickpeas is the marker of this archetype |
| Matbucha | NOT_EVALUABLE (manual review flag — see exclusion rules) |
| Eggplant spreads | Likely NOT_PREDOMINANT — eggplant is naturally high water; "water" rarely listed as separate ingredient |
| Roasted pepper spreads | WATER_EARLY possible — some may list water before peppers |

### 5.3 Expected Score Impact (Option B)

| Signal state | Products estimated | Final score impact | Grade change expected |
|-------------|-------------------|-------------------|-----------------------|
| WATER_PREDOMINANT | 5–10 | −1.6 pts avg | Unlikely — scores in 55–68 range would shift to 53–66; few grade boundaries crossed |
| WATER_EARLY | 8–15 | −0.8 pts avg | None expected |
| NOT_PREDOMINANT | 30–40 | 0 | None |
| NOT_EVALUABLE | 8–12 | 0 | None |

**Note on grade boundary risk:** The critical boundary in this corpus is B→C (70 pts). The closest product at the boundary would need to be within 1.6 pts of 70 for Option B to cause a grade change. This needs to be checked against the actual run before deployment.

### 5.4 Expected False Positive Rate

**Definition:** A false positive occurs when `WATER_PREDOMINANT` fires on a product where water position is architecturally justified — not a dilution signal.

**Primary false positive risks in this corpus:**

1. **Matbucha with added water listed** — tomatoes provide natural water; if a product also lists `מים` this may be process water, not dilution water. Expected count: 2–4 products. Mitigated by manual review flag in exclusion rules.

2. **Eggplant spread with added water** — eggplant is 92% water; added water in the ingredient list is unusual and would indicate an abnormally diluted product. Expected count: 0–1 products. Signal firing here would be a true positive, not a false positive.

3. **Products where water is listed at position 2 with chickpeas at position 1** — this is `WATER_EARLY`, not `WATER_PREDOMINANT`. If chickpeas are at position 1 and water at position 2, the signal should return `WATER_EARLY` (half penalty) or `NOT_PREDOMINANT` depending on the implementation decision. This is the most common borderline case.

**Estimated false positive rate:** 5–10% of activations. Within acceptable pilot tolerance.

---

## Section 6 — Interaction Review

### 6.1 BSIP2-061 vs. Matrix Quality (BSIP2-063)

**Nature:** Routing exclusion. Fruit matrix category is excluded from BSIP2-061 activation. The two signals do not interact — they apply to mutually exclusive routing categories.

**Status:** Resolved by exclusion gate in Section 3. No further action required for pilot.

---

### 6.2 BSIP2-061 vs. Ingredient Quality (EV-012 Fat Ratio, SEED_OIL_PRESENT)

**Nature:** Compounding signals on the same underlying product archetype.

Products that have water before chickpeas in hummus typically also have:
- Refined seed oils replacing tahini (SEED_OIL_PRESENT fires → −3 pts)
- Lower natural fat content from the tahini deficit (EV-012 fat ratio less favorable)

Both BSIP2-061 and SEED_OIL_PRESENT are symptoms of the same reconstructed architecture. They measure different things: BSIP2-061 measures ingredient position (dilution); SEED_OIL_PRESENT measures fat source quality. They are not redundant — a product could have water first but still have olive oil (not a seed oil), in which case only BSIP2-061 fires. Conversely, a product could have seed oil but chickpeas listed first, in which case only SEED_OIL_PRESENT fires.

**Pilot concern:** A product with water first AND refined seed oil AND >12 ingredients accumulates: BSIP2-061 (Option B: −1.6 pts) + SEED_OIL_PRESENT (−3 pts) + LONG_INGREDIENT_LIST (−4 pts) = −8.6 pts post-cap. Under Option C this would reach −17 pts combined with existing penalties. The −20 pt stacking cap must be confirmed to be active before Option C is deployed.

**Action:** During pilot, log the total penalty stack for every product where BSIP2-061 fires and verify it does not exceed −20 pts combined.

---

### 6.3 BSIP2-061 vs. Tahini Density (BSIP2-062)

**Nature:** Complementary signals — highly correlated activation.

Water appearing before chickpeas in hummus is structurally correlated with low tahini density. Both signals are measuring the same underlying reconstruction, from different angles:
- BSIP2-061: "water is the biggest ingredient by weight" (dilution signal)
- BSIP2-062: "tahini is absent or present in small quantity" (quality ingredient deficit)

They are measuring different observations, not the same observation. A product can theoretically have water first but still have declared tahini at 15% (positions: water, chickpeas, tahini…). In that case, BSIP2-061 fires but BSIP2-062 would reward the tahini presence.

**Recommended sequencing:** Deploy BSIP2-062 first (Implement Now priority from governance framework). Measure its corpus impact. Then deploy BSIP2-061 pilot. This allows the interactions between the two signals to be measured rather than modeled from theory.

**Action:** Do not deploy BSIP2-061 and BSIP2-062 simultaneously. Run BSIP2-062 against the corpus first. Use that as the new baseline before adding BSIP2-061.

---

### 6.4 BSIP2-061 vs. Future Dilution Signals

**Nature:** Precedent risk. BSIP2-061 is the first water/dilution detection mechanism in BSIP2. Future signals that detect other forms of dilution (yield-increasing additives, water-binding gums, moisture retention agents) must not re-detect the same water dilution event that BSIP2-061 already captures.

**Governance rule:** Any future dilution signal must include an explicit non-overlap clause with BSIP2-061. If both signals would fire on the same observation (e.g., a product with water first AND xanthan gum to retain that added water), only the stronger signal fires.

**Action:** Document this constraint in the signal registry when BSIP2-061 enters production. Not a pilot blocker.

---

### 6.5 BSIP2-061 vs. Whole Food Integrity Dimension

**Nature:** Architectural containment. Under Option B, BSIP2-061 operates within the `whole_food_integrity` dimension (4% weight). This dimension already incorporates ingredient count, reconstruction markers, and whole-food source signals.

**Existing signals in whole_food_integrity:**
- Ingredient count (LONG_INGREDIENT_LIST fires separately as post-cap penalty)
- Reconstruction markers (modified starch, reconstituted ingredients)
- Additive presence (partially — main additive signals live in `additive_quality`)

**Risk:** The dimension already penalises reconstruction through multiple routes. Adding BSIP2-061 within the same dimension adds a new input to an already composite dimension. The max 4 pt impact is contained, but the signal interaction within the dimension needs to be defined: does BSIP2-061 reduce the raw dimension score (before weighting) or apply post-weighting?

**Recommended implementation architecture:** BSIP2-061 reduces the raw `whole_food_integrity` dimension score. The final score impact is then: (reduction × 0.04). This keeps it contained and makes the dimension score directly inspectable.

---

## Section 7 — Pilot Design

### 7.1 Pilot Objective

Determine whether water-first position in the ingredient list is a reliable, low-false-positive proxy for dilution and reconstruction quality in the sauce_spread category, using the hummus corpus as the test bed.

### 7.2 Pilot Scope

| Parameter | Value |
|-----------|-------|
| Corpus | run_hummus_002 — 69 products |
| Scoring mode | Option B — within whole_food_integrity, max −4 pts |
| Categories active | sauce_spread (hummus, dips, spreads) |
| Categories excluded | As defined in Section 3 |
| Matbucha | Manual review — flagged but not auto-scored |
| Sequencing | After BSIP2-062 pilot completes and produces stable baseline |

### 7.3 Pilot Measurements Required

| Measurement | What to capture | Why |
|-------------|----------------|-----|
| Activation count | How many products return WATER_PREDOMINANT, WATER_EARLY, NOT_PREDOMINANT, NOT_EVALUABLE | Establishes empirical firing rate |
| False positive count | Products where signal fires but manual review determines water position is architecturally justified | Establishes false positive rate |
| Grade changes | Products that cross a grade boundary due to BSIP2-061 | Validates that boundary crossings are directionally correct |
| Rank shifts | How many products shift >3 positions in the rank order | Validates baseline stability |
| Penalty stack | Total post-cap penalty for each product where BSIP2-061 fires | Validates stacking cap compliance |
| Correlation with BSIP2-062 | If BSIP2-062 is deployed first: does BSIP2-061 fire on the same products that BSIP2-062 already differentiates? | Validates non-redundancy |

### 7.4 Pilot Success Criteria

For BSIP2-061 to be promoted from EXPERIMENTAL to CATEGORY_SPECIFIC and advance toward production (Option C scoring):

| Criterion | Threshold | Priority |
|-----------|-----------|----------|
| Directional accuracy | ≥85% of `WATER_PREDOMINANT` activations confirmed as genuinely diluted products via manual review | Required |
| False positive rate | ≤15% of activations on products where water position is architecturally justified | Required |
| Grade change accuracy | 100% of grade changes reviewed and confirmed as directionally correct | Required |
| Rank shifts within tolerance | ≤10% of scored products shift >5 rank positions | Required |
| Penalty stack compliance | No product exceeds −20 pts combined post-cap penalties | Required |
| No matbucha false positives | Zero `WATER_PREDOMINANT` firings on matbucha products without manual review override | Required |

### 7.5 Pilot Failure Conditions

| Failure | Condition | Action |
|---------|-----------|--------|
| High false positive rate | >30% of activations are false positives | Redesign detection logic; do not promote |
| Grade boundary instability | >5 products cross grade boundaries on a corpus where the signal should not dominate | Redesign as Option A (flag only); recalibrate |
| Unresolvable matbucha conflict | Matbucha products consistently trigger WATER_EARLY with no clear resolution rule | Add matbucha to hard exclusion list; redesign detection for tomato-based categories |
| Penalty stack overflow | Multiple products exceed −20 pts combined | Re-evaluate penalty architecture before promotion to Option C |

### 7.6 Promotion Path (Pilot → Production)

```
Pilot complete (Option B on hummus corpus)
        │
        ▼
All success criteria met?
        │
       YES → CNO sign-off → Promote to CATEGORY_SPECIFIC
        │                          │
       NO → Redesign or Research  ▼
            Further              Extend to additional corpus (tahini, nut butters)
                                        │
                                        ▼
                                All extension success criteria met?
                                        │
                                       YES → Promote scoring to Option C
                                        │
                                       NO → Remain at Option B
```

---

## Section 8 — Category Roster Summary

### Categories Activated

| Category | Activation | Expected products in current corpus |
|----------|-----------|-------------------------------------|
| Hummus | YES | ~55 products (with ingredient lists) |
| Tahini-based dips | YES | ~5 products |
| Dense vegetable dips | YES | ~8 products (eggplant, pepper spreads) |
| Dairy spreads | YES | 0 products in current corpus |
| Nut butters | YES | 0 products in current corpus |

### Categories Excluded

| Category | Exclusion type | Reason |
|----------|---------------|--------|
| Beverages | Hard exclusion | Water is the archetype matrix |
| Soups | Hard exclusion | Water is the structural base |
| Fruit purees and spreads | Hard exclusion | Defer to BSIP2-063; natural fruit water is not dilution |
| Bread | Hard exclusion | Water is a structural ingredient in bread making |
| Cereals | Hard exclusion | Water is a processing ingredient |
| Matbucha | Pilot flag (manual review) | Tomato natural water vs. added water unresolvable from label alone |
| Light vinaigrettes | Hard exclusion | Water/vinegar base is the product definition |

---

## Section 9 — Pilot Recommendation

**Proceed to pilot under the following conditions:**

1. **BSIP2-062 (Hummus Tahini Density) deploys first.** The two signals are correlated and complementary. Measuring them sequentially produces cleaner impact attribution than deploying simultaneously.

2. **Pilot is run on run_hummus_002 baseline corpus.** The 69-product hummus and savory dips corpus is the right testbed — it is the only corpus where BSIP2-061 activation categories are well-represented and the baseline is frozen.

3. **Scoring is Option B only** (within whole_food_integrity, max −4 pts). No Option C until pilot success criteria are met.

4. **Matbucha sub-corpus is manually reviewed** before any BSIP2-061 signal output is scored. The 4 matbucha products in the corpus (2 in bottom 10) are the primary false positive risk. Manual inspection of their ingredient lists against the signal logic is required before automated scoring.

5. **A CNO ruling is required before promotion to Option C.** The step from −4 pts to −10 pts is a scoring architecture change, not a signal refinement. It requires a full review of the penalty stack and a re-run of the corpus to confirm grade distribution stability.

**Target sprint:** Sprint 3, after BSIP2-062 Sprint 2 pilot produces its baseline.

---

*BSIP2-061 Water-to-Primary Ingredient Predominance — Pilot Design*
*TASK-048 — Chief Nutrition Officer — 2026-05-31*
*Architecture only. No scoring changes. No implementation.*
*Next step: await BSIP2-062 Sprint 2 results before pilot launch.*
