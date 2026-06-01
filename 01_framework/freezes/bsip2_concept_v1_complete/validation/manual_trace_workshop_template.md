# Manual Trace Workshop Template

**Purpose:** A structured framework for manually tracing BSIP2 scoring for a product before implementation begins. Running 40–50 products through this template catches specification errors, unresolved interaction conflicts, and threshold calibration problems that would otherwise be discovered only after implementation — when they are far more expensive to correct.

**How to use:** Complete one copy of this template per product. Products should be drawn primarily from the golden products suite (`golden_products_suite.md`) and edge case catalog (`edge_case_catalog.md`). At least 40 products should be traced before implementation begins.

---

## Template

---

### PRODUCT IDENTIFICATION

**Product name:**
**Category (inferred):**
**Category confidence (est.):** ☐ High (>0.80) ☐ Medium (0.50–0.79) ☐ Low (<0.50)
**Secondary category (if ambiguous):**
**Evaluation status:** ☐ Standard ☐ Context-limited ☐ Out of scope

---

### SECTION 1 — RAW SIGNALS (L1 Observed Facts)

*Enter values from the product record. Mark absent fields explicitly.*

| Field | Value | Present? |
|-------|-------|---------|
| Energy (kcal/100g) | | ☐ Yes ☐ No |
| Protein (g/100g) | | ☐ Yes ☐ No |
| Total carbohydrates (g/100g) | | ☐ Yes ☐ No |
| of which sugar (g/100g) | | ☐ Yes ☐ No |
| Total fat (g/100g) | | ☐ Yes ☐ No |
| of which saturated fat (g/100g) | | ☐ Yes ☐ No |
| Fiber (g/100g) | | ☐ Yes ☐ No |
| Sodium (mg/100g) | | ☐ Yes ☐ No |
| Ingredient list | | ☐ Yes ☐ No |
| Israeli red labels | | N/A ☐ None ☐ Sugar ☐ Sat fat ☐ Sodium ☐ 2+ |
| Barcode | | |
| BSIP1 trust level | | ☐ High ☐ Medium ☐ Low ☐ Unknown |

**Data consistency checks:**
- Sugar ≤ Total carbohydrates? ☐ Yes ☐ No ☐ Cannot check
- Saturated fat ≤ Total fat? ☐ Yes ☐ No ☐ Cannot check
- Energy in plausible range (20–700 kcal)? ☐ Yes ☐ No ☐ Cannot check

---

### SECTION 2 — DERIVED METRICS (L2)

*Compute from L1 values.*

| Metric | Formula | Value |
|--------|---------|-------|
| Fat from kcal (%) | (fat × 9) / kcal × 100 | |
| Saturated fat fraction | sat fat / total fat | |
| Sugar-to-carb ratio | sugar / carbs | |
| Protein-per-kcal ratio | protein / kcal | |
| Ingredient count | count distinct ingredients | |
| Additive marker count | count detected additive markers (list below) | |

**Additive markers detected (list each):**
1.
2.
3.
4.
5.
6.

---

### SECTION 3 — INFERRED CLASSIFICATIONS (L3)

*These require judgment; note confidence level for each.*

| Classification | Value | Confidence | Basis |
|---------------|-------|------------|-------|
| Product category | | ☐ H ☐ M ☐ L | |
| NOVA level (1–4) | | ☐ H ☐ M ☐ L | |
| HP pattern: fat-sugar | ☐ Yes ☐ No | | fat ≥ 30% kcal AND sugar ≥ 20g? |
| HP pattern: fat-sodium | ☐ Yes ☐ No | | fat ≥ 25% kcal AND sodium ≥ 300mg? |
| HP pattern: refined carb + fat | ☐ Yes ☐ No | | |
| HP pattern: crunch-sweet | ☐ Yes ☐ No | | sugar ≥ 20g AND fiber ≤ 3g (cereal)? |
| Protein source | ☐ Whole food ☐ Isolate ☐ Mixed | | |
| Sweetener presence | ☐ Yes ☐ No | | |
| Whole grain presence | ☐ Yes ☐ No | | |
| Seed oil presence | ☐ Yes ☐ No | | |
| Protein isolate marker | ☐ Yes ☐ No | | |
| Multiple added sugar sources | ☐ Yes ☐ No | | count: |

---

### SECTION 4 — CONFIDENCE CALCULATION

*Start at 100 and subtract.*

| Factor | Reduction | Apply? | Running total |
|--------|-----------|--------|--------------|
| Starting confidence | — | — | 100 |
| Energy absent | −10 | ☐ | |
| Protein absent | −10 | ☐ | |
| Carbohydrates absent | −10 | ☐ | |
| Fat absent | −10 | ☐ | |
| Fiber absent | −5 | ☐ | |
| Sodium absent | −5 | ☐ | |
| Ingredient list absent | −25 | ☐ | |
| Sugar > carbs | −20 | ☐ | |
| Sat fat > fat | −20 | ☐ | |
| Energy outside range | −10 | ☐ | |
| Low NOVA confidence | up to −10 | ☐ | |
| Low category confidence | up to −15 | ☐ | |
| **Final confidence** | | | **=** |

**Confidence band:** ☐ High (≥80) ☐ Medium (60–79) ☐ Low (40–59) ☐ Insufficient (<40)

**Confidence ceiling active?**
- Insufficient: score ≤ 50 ☐
- Low: score ≤ 70 ☐
- No ceiling ☐

---

### SECTION 5 — DIMENSION SCORING (preliminary)

*Estimate each dimension score based on current specification. Mark where exact formula is uncertain.*

| Dimension | Weight | Est. Score (0–100) | Key signals driving it | Formula certain? |
|-----------|--------|-------------------|----------------------|-----------------|
| Processing Quality | 15% | | NOVA: | ☐ Yes ☐ Approx |
| Nutrient Density | 15% | | protein:, fiber:, minerals: | ☐ Yes ☐ Approx |
| Calorie Density Quality | 15% | | kcal:, category table: | ☐ Yes ☐ Approx |
| Glycemic Quality | 12% | | sugar:, fiber:, whole grain: | ☐ Yes ☐ Approx |
| Protein Quality | 10% | | source:, quantity: | ☐ Yes ☐ Approx |
| Additive Quality | 10% | | marker count:, sweetener: | ☐ Yes ☐ Approx |
| Satiety Support | 6% | | protein:, fiber: | ☐ Yes ☐ Approx |
| Fat Quality | 8% | | sat fat:, sat frac: | ☐ Yes ☐ Approx |
| Regulatory Quality | 5% | | red labels: | ☐ Yes ☐ Approx |
| Whole Food Integrity | 4% | | NOVA:, complexity: | ☐ Yes ☐ Approx |
| Hyper-Palatability | | | patterns: | ☐ Yes ☐ Approx |

**Weighted dimension score (pre-guardrail):**
Sum of (dimension score × weight) for all dimensions = ___

---

### SECTION 6 — GUARDRAIL RULE EVALUATION (L4)

*Work through each applicable concern family. Mark which rules fire.*

#### SUGAR_LOAD

| Rule | Threshold | Value | Fires? | Cap/Penalty |
|------|-----------|-------|--------|-------------|
| HIGH_CAL_HIGH_SUGAR_SEVERE | kcal≥500 AND sugar≥25g | kcal=___ sugar=___ | ☐ | Cap 50 |
| HIGH_CAL_HIGH_SUGAR_MODERATE | kcal≥470 AND sugar≥20g | | ☐ | Cap 60 |
| HIGH_SUGAR_25G_PLUS | sugar≥25g | | ☐ | Cap 60 |
| SNACK_BAR_HIGH_CAL_SUGAR | snack bar, kcal≥470, sugar≥15g | | ☐ | Cap 60 |
| SNACK_BAR_RED_SUGAR_LABEL | snack bar + red sugar label | | ☐ | Cap 55 |
| ISRAELI_RED_LABEL_1 (sugar) | red label = sugar | | ☐ | Cap 55 |
| ISRAELI_RED_LABELS_2_PLUS (sugar) | 2+ labels incl sugar | | ☐ | Cap 45 |
| MULTIPLE_ADDED_SUGAR_MARKERS | 2+ added sugar sources | | ☐ | Penalty −5 |
| HIGH_CAL_HIGH_SUGAR_SOFT | kcal≥430 AND sugar≥15g | | ☐ | Penalty −5 |
| HP_FAT_SUGAR_COMBO | fat-sugar pattern | | ☐ | HP penalty |
| HP_CRUNCH_SWEET_COMBO | crunch-sweet pattern | | ☐ | HP penalty |

**Coordination outcome:**
- Surviving cap (strictest): ___
- Winner penalty (largest, at full): ___
- Supporting penalties (scaled to 40%): ___
- Total sugar penalty before budget: ___
- After budget clamp (max 10): ___

#### CALORIE_LOAD

| Rule | Threshold | Fires? | Cap/Penalty |
|------|-----------|--------|-------------|
| HIGH_CAL_LOW_SATIETY_SEVERE | kcal≥500 AND protein<6g AND fiber<3g | ☐ | Cap 55 |
| SNACK_BAR_HIGH_CAL | snack bar, kcal≥430 | ☐ | Cap 70 |
| HIGH_CAL_LOW_SATIETY_SOFT | kcal≥450 AND protein<8g AND fiber<5g | ☐ | Penalty −6 |

**Coordination outcome:**
- Surviving cap (strictest): ___
- Penalty after coordination: ___
- After budget clamp (max 8): ___

#### PROCESSING_LOAD

| Rule | Threshold | Fires? | Cap/Penalty |
|------|-----------|--------|-------------|
| NOVA_PROXY_4_ULTRA_PROCESSED | NOVA 4 | ☐ | Cap 60 |
| ADDITIVE_MARKERS_5_PLUS | 5+ markers | ☐ | Cap 55 |
| ADDITIVE_MARKERS_3_PLUS | 3–4 markers | ☐ | Cap 65 |
| NOVA_PROXY_3_PROCESSED | NOVA 3 | ☐ | Cap 75 |
| LONG_INGREDIENT_LIST | >12 ingredients | ☐ | Penalty −4 |

**Coordination outcome:**
- Surviving cap (strictest): ___
- Penalty after coordination: ___
- After budget clamp (max 12): ___

#### SODIUM_LOAD

| Rule | Threshold | Fires? | Cap/Penalty |
|------|-----------|--------|-------------|
| HIGH_SODIUM_700MG_PLUS | sodium≥700mg | ☐ | Cap 60 |
| HP_FAT_SODIUM_COMBO | fat≥25% kcal AND sodium≥300mg | ☐ | HP penalty |

**Coordination outcome:**
- Surviving cap: ___
- Penalty at full or 40%: ___
- After budget clamp (max 8): ___

#### FAT_QUALITY

| Rule | Threshold | Fires? | Cap/Penalty |
|------|-----------|--------|-------------|
| ISRAELI_RED_LABEL_1 (sat fat) | red label = sat fat | ☐ | Cap 55 |
| SEED_OIL_PRESENT | seed oil in ingredients | ☐ | Penalty −3 |

**Coordination outcome:**
- Surviving cap: ___
- Penalty after coordination: ___
- After budget clamp (max 8): ___

#### SWEETENER (independent — not in CONCERNS graph)

| Rule | Fires? | Effect |
|------|--------|--------|
| SWEETENER_PRESENT | ☐ | Cap 70 (independent) |

#### FLOORS AND VETOES

| Rule | Fires? | Effect |
|------|--------|--------|
| Trans fat veto | ☐ | Score = 0 |
| NOVA 1 single ingredient floor | ☐ | Min score 75 |
| Whole food fat NOVA 1–2 floor | ☐ | Min score 65 |

---

### SECTION 7 — SCORE ASSEMBLY

*Assemble the final score step by step.*

**Step 1: Pre-guardrail weighted dimension score:** ___

**Step 2: Apply concern coordination outcomes**
- Effective sugar-load cap (after coordination): ___
- Effective calorie-load cap: ___
- Effective processing-load cap: ___
- Effective sodium-load cap: ___
- Effective fat-quality cap: ___
- Sweetener cap: ___
- **Binding cap (strictest of all above):** ___

**Step 3: Apply coordinated penalties**
- Sugar family total penalty (after budget): ___
- Calorie density family total penalty (after budget): ___
- Processing family total penalty (after budget): ___
- Sodium family total penalty (after budget): ___
- Fat quality family total penalty (after budget): ___
- Hyper-palatability family total penalty (after budget): ___
- Other families: ___
- **Total penalty (sum):** ___

**Step 4: Score before floor and confidence**
min(dimension score, binding cap) − total penalty = ___

**Step 5: Apply floors**
- If NOVA 1 single ingredient: min = 75
- If whole food fat NOVA 1–2: min = 65
- **Score after floors:** max(Step 4 result, applicable floor) = ___

**Step 6: Apply confidence ceiling**
- Confidence ceiling active? ☐ Yes (cap at ___ ) ☐ No
- **Final score:** min(Step 5 result, confidence ceiling) = ___

**Final score:** ___
**Grade:** ☐ A (85–100) ☐ B (70–84) ☐ C (55–69) ☐ D (40–54) ☐ E (0–39)

---

### SECTION 8 — CROSS-CHECK AGAINST EXPECTED BEHAVIOR

**Expected qualitative behavior (from golden products suite or edge case catalog):**

**Does the traced score match?** ☐ Yes ☐ No ☐ Partially

**If no — what is wrong?**

---

### SECTION 9 — SECONDARY CATEGORY SIMULATION

**Secondary category:** ___

**Repeat calorie density dimension score with secondary category table:**
- kcal: ___, secondary category table score: ___
- Secondary category caps that would apply:

**Score delta (primary − secondary):** ___
**Classification sensitivity:** ☐ Low (<10) ☐ Medium (10–20) ☐ High (>20)

If HIGH: this product must be flagged in the output as classification-sensitive.

---

### SECTION 10 — USER-FACING EXPLANATION

*Draft the explanation a user should see for this product. Maximum three primary signals.*

**Dominant driver:** (one sentence)

**Supporting signal 1:** (one phrase)

**Supporting signal 2:** (one phrase)

**Confidence note (if confidence < high):**

**Category context note (if classification-sensitive or context_limited):**

---

### SECTION 11 — TENSIONS AND CONTRADICTIONS IDENTIFIED

*Note any place where the specification produced an unexpected, contradictory, or unexplainable result.*

**Tension 1:**
- Rule or threshold involved:
- Why it feels wrong:
- Proposed resolution:

**Tension 2:**
- Rule or threshold involved:
- Why it feels wrong:
- Proposed resolution:

**Tension 3:**

---

### SECTION 12 — TRACE METADATA

**Traced by:**
**Date:**
**Time to complete:**
**Specification version:** bsip2_concept_v1
**Source product:** ☐ Golden products suite ☐ Edge case catalog ☐ Other (specify):
**Difficulty:** ☐ Straightforward ☐ Several judgment calls ☐ Multiple specification gaps
**Flag for architecture review?** ☐ Yes ☐ No

---

## Workshop Process Notes

**Target volume:** 40–50 products minimum before implementation. Suggested distribution:
- 10 SHOULD SCORE HIGH products (confirm floors and positive signals work)
- 10 SHOULD SCORE LOW products (confirm caps and penalties work)
- 10 SHOULD SCORE MEDIUM products (confirm discrimination works)
- 10 SHOULD BE NUANCED products (confirm tradeoff representation works)
- 10+ edge cases (confirm category and NOVA classification edge cases are handled)

**Priority products** (complete these first):
1. Dates — floor vs. natural sugar cap interaction
2. Coconut oil — saturated fat cap vs. whole-food floor
3. Brined olives — sodium cap vs. whole-food floor
4. Date-nut bar — category classification sensitivity
5. Diet chocolate mousse — structural emptiness test
6. Plain almonds — baseline high-quality whole food
7. Sugary granola bar — canonical low-score product
8. Coke Zero — sweetener cap + NOVA 4 + zero nutrition
9. Plain Greek yogurt — dairy protein category positive
10. Instant noodles — sodium + processing + low satiety combination

**After completing traces:**
- Compile all Section 11 tensions across all products
- Identify the three most common tension types
- Bring the three most common tensions to an architecture review before implementation begins
- Any product with Section 9 classification sensitivity rated HIGH must have its category assignment manually reviewed before the product enters the live scoring pipeline
