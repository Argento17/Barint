# Score Resolution Contract

**Document ID:** SRC-v1  
**Date:** 2026-05-17  
**Specification version:** bsip2_concept_v1  
**Source:** Manual Trace Workshop Results (validation/manual_trace_workshop_results.md)  
**Status:** Pre-implementation architectural contract — not production code

**Purpose:** Resolve the seven classes of architectural contradiction discovered during the adversarial manual trace workshop. This document defines explicit resolution rules that supersede any ambiguity in prior specification documents when the two conflict.

---

## Scope and Authority

This contract modifies the behavior of the scoring pipeline at the specification level. All future implementation work must respect these resolutions. Where this contract conflicts with earlier specification documents, this contract governs.

This contract does NOT:
- Add new scoring dimensions
- Tune thresholds numerically (threshold calibration remains a testing-phase activity)
- Introduce production scoring code
- Change the concern coordination logic for rules that continue to apply

---

## Resolution 1 — Floor–Cap Hierarchy (SRC-01)

### The Problem

Four products in the workshop produced a mathematical conflict: a guardrail cap produced a score lower than the applicable whole-food floor. The prior specification contained no rule for resolving this conflict.

### Resolution Principle

Whole-food floors are NOT unconditional overrides. Their authority depends on whether the cap that is conflicting was designed for the product class in question.

Caps are divided into two classes for floor-interaction purposes:

**Class A — Architecture-mismatch caps**  
Caps designed for engineered, processed, or additive-loaded products that fire on whole foods only by compositional coincidence. The whole-food floor unconditionally overrides these caps when a product is NOVA 1 or NOVA 2.

Class A caps:
- NOVA_PROXY_4_ULTRA_PROCESSED (cap 60) — cannot fire on NOVA 1; this conflict is moot
- NOVA_PROXY_3_PROCESSED (cap 75) — cannot fire on NOVA 1; this conflict is moot
- ADDITIVE_MARKERS_3_PLUS, ADDITIVE_MARKERS_5_PLUS — cannot fire on additive-free whole foods; moot
- LONG_INGREDIENT_LIST penalty — cannot fire on single-ingredient products; moot
- HP_FAT_SUGAR_COMBO, HP_FAT_SODIUM_COMBO, HP_CRUNCH_SWEET_COMBO — see SRC-06 for gate logic

In practice, Class A conflicts do not occur for NOVA 1 products because the rules cannot fire. The override rule exists as documentation of intent and as a guard against future rule additions that might reach NOVA 1 products unexpectedly.

**Class B — Physiological load caps**  
Caps that represent real nutritional concerns that exist even in whole foods. These are NOT overridden by the whole-food floor.

Class B caps:
- HIGH_CAL_HIGH_SUGAR_SEVERE, HIGH_CAL_HIGH_SUGAR_MODERATE, HIGH_SUGAR_25G_PLUS (see SRC-02 for exemption routing)
- ISRAELI_RED_LABEL_1 (both sugar and saturated fat contexts), ISRAELI_RED_LABELS_2_PLUS
- HIGH_CAL_LOW_SATIETY_SEVERE, HIGH_CAL_LOW_SATIETY_SOFT (see SRC-03 for gating)
- HIGH_SODIUM_700MG_PLUS (see SRC-03 for context-limited handling)
- SNACK_BAR_HIGH_CAL, SNACK_BAR_HIGH_CAL_SUGAR, SNACK_BAR_RED_SUGAR_LABEL

### Contextual Moderation for Physiological Caps on Whole Foods

When a Class B cap fires on a NOVA 1 single-ingredient product, the following moderation rule applies in place of the full whole-food floor:

**Physiological moderation minimum:** 60

The score may not go below 60 for a NOVA 1 single-ingredient product when the only binding cap is a Class B cap.

Rationale: The cap represents a genuine concern. The NOVA 1 status does not eliminate the concern — but it does change the severity interpretation. A whole food with a physiological load characteristic occupies a different risk position than an engineered product with the same characteristic. Score range 60–74 for a whole food with a physiological concern communicates: "high-quality food source with a genuine nutritional consideration," which is more accurate than either "Grade A" (floor wins entirely) or "Grade D" (cap wins entirely).

**The full NOVA 1 floor (75) applies when:**
- No Class B caps fire on the product, OR
- All Class B caps that would have fired are exempted by SRC-02 (natural sugar routing) or SRC-03 (category gating)

**The physiological moderation minimum (60) applies when:**
- At least one Class B cap fires and is not exempted by other resolutions

**The full cap value applies when:**
- A Class B cap fires on a NOVA 3 or NOVA 4 product (no floor protection)
- A NOVA 1–2 product has 2+ Israeli red labels (ISRAELI_RED_LABELS_2_PLUS): in this case, the moderation minimum drops to 50, reflecting that two concurrent regulatory failures represent a genuine compound concern even in whole foods

### Score Assembly Change

Step 5 of the existing score assembly (Apply floors) is replaced by:

```
Step 5 — Apply floor with cap classification check:
  binding_caps = set of caps that determined the final score
  class_a_only = all binding caps are Class A
  class_b_present = any binding cap is Class B
  
  if class_a_only OR no_binding_caps:
    apply full NOVA 1 floor (75) or NOVA 1–2 whole food fat floor (65)
  
  elif class_b_present AND product is NOVA 1 single-ingredient:
    apply physiological moderation minimum (60)
    unless ISRAELI_RED_LABELS_2_PLUS fires → minimum is 50
  
  else:
    no floor applies
```

---

## Resolution 2 — Natural vs. Added Sugar Routing (SRC-02)

### The Problem

Sugar caps (`HIGH_SUGAR_25G_PLUS`, `HIGH_CAL_HIGH_SUGAR_SEVERE`, `ISRAELI_RED_LABEL_1`) are calibrated for products where elevated sugar represents an engineered or refined addition. They fire on whole dried fruit (dates, figs, raisins) where the sugar is intrinsic to the food matrix and co-present with fiber, micronutrients, and a coherent food structure. A simple "natural sugar exempt" rule is not appropriate because the sugar-context continuum is not binary.

### Sugar Context Classification (SC)

Each product is assigned a sugar context class at L3 inference before sugar cap evaluation. The class is determined by the source of the sugar in the ingredient list and the product's NOVA classification:

| Class | Description | Detection criteria |
|-------|-------------|-------------------|
| SC-1 | Intact whole-fruit sugar | NOVA 1, single-ingredient fresh or dried fruit, no added sweetener or syrup markers |
| SC-2 | Dried/concentrated whole-fruit sugar, multi-ingredient | NOVA 1–2, whole fruit is the primary or first ingredient, no added sugar markers detected, ingredient list reads as whole-food combination |
| SC-3 | Liberated or juice-extracted sugar | Fruit juice as primary ingredient (not fruit), OR product where fruit has been juiced/extracted — fiber absent despite fruit origin |
| SC-4 | Fruit concentrate or fruit syrup as a sweetener ingredient | date syrup, fruit juice concentrate, agave syrup, or similar listed as an ingredient in a multi-ingredient product (not as the primary whole-food component) |
| SC-5 | Refined added sugar | sugar, cane sugar, high-fructose corn syrup, glucose syrup, sucrose, or equivalent as a listed ingredient |

**If multiple sugar sources are present, the highest-severity class governs.** A product with whole dates AND date syrup is SC-4. A product with fruit AND refined sugar is SC-5.

### Cap Treatment by Sugar Context Class

| Sugar class | HIGH_SUGAR_25G_PLUS | HIGH_CAL_HIGH_SUGAR_SEVERE | HIGH_CAL_HIGH_SUGAR_MODERATE | ISRAELI_RED_LABEL_1 (sugar) |
|-------------|--------------------|--------------------------|-----------------------------|----------------------------|
| SC-1 | Suspended | Suspended | Suspended | Suspended — regulatory signal noted in output, cap not applied |
| SC-2 | Threshold raised to 40g | Threshold raised to sugar≥40g | Threshold raised to sugar≥35g | Applied (cannot suspend a regulatory label) |
| SC-3 | Applied at standard threshold | Applied | Applied | Applied |
| SC-4 | Applied at standard threshold | Applied | Applied | Applied |
| SC-5 | Applied at standard threshold | Applied | Applied | Applied |

**SC-1 rationale for ISRAELI_RED_LABEL_1 suspension:** The Israeli red label on a single-ingredient dried fruit is a regulatory signal accurately describing the product's sugar concentration. BSIP2 notes the label in the output record. The cap is suspended because the label was not designed to evaluate single-ingredient whole foods — it was calibrated for the general packaged food population — and applying a cap calibrated for that population to a NOVA 1 whole fruit produces a category error, not a meaningful analytical signal.

**SC-2 raised threshold rationale:** Dried fruit has genuinely elevated sugar per 100g as a consequence of water removal. The concentration effect is real but not equivalent to added sugar. Raising the firing threshold by approximately 60% (from 25g to 40g) partially accounts for the concentration effect while preserving sensitivity to extreme cases (dates at 63g still fire the softened SC-2 version at 40g threshold).

### Multi-Ingredient Sugar Classification Rule

For multi-ingredient products where the sugar source requires ingredient-level analysis:
1. Scan ingredient list for SC-4 and SC-5 markers first. If any found → SC-4 or SC-5 respectively.
2. If no SC-4/SC-5 markers, check if primary ingredient is whole fruit → SC-2.
3. If primary ingredient is fruit juice or fruit extract → SC-3.
4. Single-ingredient whole/dried fruit → SC-1.

---

## Resolution 3 — Context-Limited Product Handling (SRC-03)

### The Problem

Standard per-100g scoring is systematically misleading for product classes where typical consumption quantity is well below 100g, or where the per-100g nutritional profile is not representative of the dietary contribution. The prior specification noted `context_limited` status in `evaluation_scope.md` but did not define which guardrail rules are gated for context-limited products or what the output format is.

### Context-Limited Product Classes and Gating Rules

**Cooking oils and pure fats** (including coconut oil, olive oil, butter, ghee):
- Context note: "Typically consumed in 10–20g portions. Per-100g calorie density and satiety metrics do not reflect dietary contribution from typical use."
- Gated rules: `HIGH_CAL_LOW_SATIETY_SEVERE` and `HIGH_CAL_LOW_SATIETY_SOFT` are suspended. Rationale: satiety rules are designed for high-calorie products that fail to deliver satiety nutrients. A cooking fat is definitionally protein-free and fiber-free — this is not a satiety design failure but a category property. Applying satiety rules to a cooking fat produces category errors, not analytical signals.
- Rules that continue to apply: `ISRAELI_RED_LABEL_1` (saturated fat), `SEED_OIL_PRESENT`. Fat quality concerns are real and per-100g is meaningful for fat composition evaluation.
- Grade handling: grade is displayed with a context annotation: "Grade reflects per-100g composition; portion context applies."

**Condiments — high-concentration** (soy sauce, fish sauce, oyster sauce, miso paste, hot sauce):
- Context note: "Consumed in 5–15g portions. Sodium concentration per 100g is not reflective of dietary sodium load from typical use."
- Gated rules: `HIGH_SODIUM_700MG_PLUS` cap is softened — penalty applies but cap does not. The product is marked `context_limited` and the sodium concern is surfaced as a contextual note rather than a binding cap.
- Grade handling: grade shown with asterisk and context note.

**Brined and pickled foods** (olives, pickles, capers, preserved lemons):
- Context note: "Sodium reflects preservation brine. Not all sodium in the per-100g figure is consumed; brine is typically not eaten."
- Gated rules: `HIGH_SODIUM_700MG_PLUS` cap applies but at 70% weight (the cap binds, but the floor interaction uses the physiological moderation minimum from SRC-01 rather than the full cap value). `HP_FAT_SODIUM_COMBO` is subject to the HP gate (SRC-06).
- Grade handling: grade displayed with brine context note.

**Concentrated sweeteners** (honey, maple syrup, date syrup, molasses):
- Context note: "Consumed in small quantities (5–20g). Per-100g sugar analysis reflects concentration, not typical consumption load."
- Gated rules: `HIGH_SUGAR_25G_PLUS` fires but is flagged as context-sensitive. The cap applies at 80% weight. Sugar context classification also applies (honey = SC-1, date syrup = SC-4, etc.).
- Grade handling: grade shown with context note.

**Beverages**:
- Per-100g is already appropriate for beverages. No additional gating.
- Exception: meal replacement beverages and electrolyte drinks → `context_limited` (see `evaluation_scope.md`).

### Output Format for Context-Limited Products

```
{
  "score": <integer>,
  "grade": "<letter> *",        // asterisk if context_flag is active
  "context_flag": "<category>", // e.g., "cooking_oil", "brined_food", "condiment_high_concentration"
  "context_note": "<string>",   // human-readable explanation of the per-100g limitation
  "score_reliability": "standard" | "context_limited"
}
```

When `score_reliability` is `context_limited`, the UI must display the context note alongside the grade. The grade is not suppressed — it is annotated.

---

## Resolution 4 — Structural Emptiness Gate (SRC-04)

### The Problem

The calorie density dimension awards its highest scores to products with very low calorie density. This is appropriate for whole foods with low calorie density. It is not appropriate for engineered products where the low calorie density is achieved by removing all food structure — protein, fat, fiber — and replacing it with water, modified starch, sweeteners, and flavouring systems. The current dimension cannot distinguish between the two.

Coke Zero at ≤10 kcal/100g scores 95/100 on a dimension weighted at 15% — the highest possible score on the highest-weighted dimension — not because it is nutritionally excellent, but because it contains almost nothing.

### Structural Emptiness Detection (L3 Inference)

A product is classified as **structurally empty** if ALL of the following conditions hold:

1. Calorie density < 80 kcal/100g (or < 20 kcal/100g for beverages)
2. Protein < 3g/100g
3. Fiber < 1.5g/100g
4. Fat < 2g/100g
5. At least one of: sweetener present, additive marker count ≥ 2, NOVA classification ≥ 3

Condition 5 is the discrimination gate. It distinguishes engineered-empty products (Coke Zero, diet mousse, zero-sugar jelly) from naturally low-nutrient whole foods (cucumber, plain broth, herbal tea). A cucumber satisfies conditions 1–4 but fails condition 5: no sweetener, no additives, NOVA 1.

### Dimension Score Adjustments for Structurally Empty Products

When `structurally_empty = true`:

**Calorie density dimension:** Score is capped at 50 (neutral value). The product does not earn calorie density credit for containing almost no food. Rationale: low calorie density is a quality signal when it reflects a food's natural composition or genuine nutritional design. It is not a quality signal when it reflects the absence of food structure.

**Glycemic quality dimension:** No adjustment beyond existing sweetener signals. The SWEETENER_PRESENT cap (70) already limits the ceiling. The glycemic dimension naturally scores low for structurally empty products because there is no glycemic structure to evaluate.

**Fat quality dimension:** If total fat < 0.5g/100g, the fat quality dimension returns a neutral score (50). The product has no fat composition to evaluate. A near-zero fat product cannot earn positive fat quality credit for having no fat — the absence of a concern is not the presence of a positive.

**Note:** This gate does NOT add a new penalty. It prevents the erroneous award of positive dimension credit for structural absence. The guardrail rules continue to apply normally and typically dominate the score for NOVA 4 + sweetener products anyway.

---

## Resolution 5 — Penalty-on-Low-Base Control (SRC-05)

### The Problem

When a product's weighted dimension score is already very low (28–40), applying the full suite of coordinated penalties can push the final score into single digits. Family budget clamps limit penalty totals per family, but multiple families can apply simultaneously. The result is that genuinely poor products reach scores like 11 or 14 — values that carry no additional informational content compared to 18 or 22 and make the grade scale meaningless below Grade E.

Grade E (score < 40) is not a precision zone. It communicates "this product has serious structural quality concerns." Whether the score is 11 or 28 does not add information; it adds noise.

### Relative Penalty Budget

After concern coordination and family budget clamping (existing rules unchanged), apply a relative penalty cap:

**Total coordinated penalties may not exceed 50% of the pre-penalty score.**

The pre-penalty score is the weighted dimension score after cap application but before penalty application.

| Pre-penalty score | Maximum total penalties |
|-------------------|------------------------|
| ≥ 70 | Full penalty budget (existing family clamps govern) |
| 50–69 | min(full penalty total, pre-penalty score × 0.50) |
| 30–49 | min(full penalty total, pre-penalty score × 0.50) |
| < 30 | min(full penalty total, pre-penalty score × 0.45) |

When the relative cap is binding, penalties are scaled proportionally: each family's penalty is reduced by the same fraction until the total reaches the relative cap.

**Absolute floor for non-veto products:**
- No product without a trans fat veto scores below 10.
- No product without ISRAELI_RED_LABELS_2_PLUS AND NOVA 4 simultaneously active scores below 15.

### When Grade E Is Appropriate

Grade E (score < 40) is architecturally appropriate when:
- A trans fat veto fires (score = 0): unambiguous product failure
- ISRAELI_RED_LABELS_2_PLUS fires AND the product is NOVA 4: compound regulatory + processing failure
- A binding cap at 45 or below fires AND the product has a weighted dimension score below 45 before cap application: the product is poor on both structural and guardrail dimensions simultaneously

Grade E from penalties alone (without a binding cap below 45 and without veto conditions) is not appropriate. A product that scores 35 on dimensions and receives 20 points of penalties should not reach 15 — the cap at 40 and the relative penalty budget together prevent this.

**This resolution does not protect products that deserve Grade E.** Instant noodles and sugary granola bars remain Grade E. The resolution prevents single-digit scores that have no communicative value, not the Grade E classification itself.

---

## Resolution 6 — Hyper-Palatability Applicability Gate (SRC-06)

### The Problem

The HP penalty engine fires based on compositional patterns (fat × sugar, fat × sodium, crunch × sweet). These patterns were calibrated against engineered products where the combination was deliberately constructed to override satiety signaling. They misfire on whole-food products where the same compositional coincidence arises from the natural properties of the ingredients:

- HP_FAT_SUGAR_COMBO fires on a date-nut bar (dates provide sugar; nuts provide fat; no palatability engineering involved)
- HP_FAT_SODIUM_COMBO fires on brined olives (olives provide fat; brine provides sodium; this is preservation, not palatability engineering)

### HP Applicability Gate

HP patterns are gated by NOVA classification at L3:

| NOVA level | HP penalty weight |
|------------|------------------|
| NOVA 1 | 0% — HP patterns do not fire |
| NOVA 2 | 0% — HP patterns do not fire |
| NOVA 3 | 50% of standard HP penalty weight |
| NOVA 4 | 100% of standard HP penalty weight |

**Rationale:** The behavioral hypothesis embedded in HP rules (deliberate palatability engineering to override satiety) is applicable to products built through industrial formulation (NOVA 3–4). It is not applicable to products that are minimally processed combinations of whole-food ingredients. NOVA 1–2 classification is the practical gate for this distinction.

**NOVA classification confidence applies:** If NOVA confidence is low (< 0.60), HP penalties apply at 50% regardless of NOVA level. Low-confidence NOVA 3–4 classification should not produce full HP penalties.

**HP_CRUNCH_SWEET_COMBO** is restricted to cereal-category products only. It does not apply to whole-food bars, fruit, or nut-seed products regardless of NOVA level.

### Score Assembly Change

HP pattern evaluation in guardrail Section 6 of the template is modified:

```
for each HP pattern that compositionally fires:
  nova_weight = get_nova_hp_weight(product.nova_level, product.nova_confidence)
  effective_penalty = base_hp_penalty × nova_weight
  if effective_penalty > 0:
    add to hyper_palatability family penalties
```

---

## Resolution 7 — Category Confidence Severity Modulation (SRC-07)

### The Problem

Category misclassification is the largest single source of score instability. A 30-point swing from `snack_bar_granola` to `whole_food_fat` is possible for the same product with no measurement change. When category confidence is low or medium, the system should communicate uncertainty rather than presenting a confident grade derived from an uncertain classification.

### Confidence-Modulated Category Behavior

**High confidence (> 0.80):** Standard scoring. Category-specific calorie density table and category-specific caps apply normally.

**Medium confidence (0.50–0.79):**
- Category-specific calorie density table: threshold for each tier is relaxed by 10% (moving the tier boundary upward, making the score slightly more generous)
- Category-specific caps: threshold for firing is raised by 10% (e.g., SNACK_BAR_HIGH_CAL fires at kcal≥430×1.1=473 rather than 430)
- Secondary category simulation: mandatory. The scoring pipeline must run a parallel score using the secondary category table.
- Output must include: `category_confidence`, `secondary_category`, `score_delta`, `classification_sensitivity` (see below)

**Low confidence (< 0.50):**
- Category-specific calorie density table: default category table is substituted
- Category-specific caps: suspended. Only product-agnostic caps apply (HIGH_SUGAR_25G_PLUS, HIGH_SODIUM_700MG_PLUS, etc.)
- Output: `category = "uncertain"`, grade shown with double asterisk (**) and classification uncertainty note
- Secondary category simulation: mandatory

### Classification Sensitivity Thresholds

After running the secondary category simulation:

| Score delta (primary − secondary) | Classification sensitivity |
|----------------------------------|---------------------------|
| < 10 points | Low — score is robust to category uncertainty |
| 10–20 points | Medium — category uncertainty materially affects interpretation |
| > 20 points | High — product must be flagged; manual category review required before live scoring |

When classification sensitivity is High, the output must include: `"flag": "manual_category_review_required"`. Products with this flag must not appear in the public scoring pipeline until the category assignment has been manually reviewed.

### Output Fields Added

```
{
  "category": "<primary>",
  "category_confidence": <float>,
  "secondary_category": "<secondary>",
  "score_delta": <integer>,
  "classification_sensitivity": "low" | "medium" | "high",
  "classification_note": "<string>",
  "flag": "manual_category_review_required" | null
}
```

---

## Updated Score Assembly Order

The full score assembly sequence incorporating all resolutions:

**Stage 0 — Pre-scoring classification (new)**
1. Assign `evaluation_status` (standard / context_limited / out_of_scope) — gates the entire pipeline
2. If `out_of_scope`: return null score with explanation note
3. Assign `context_flag` and `context_note` if applicable (SRC-03)
4. Assign sugar context class SC-1 through SC-5 (SRC-02)
5. Detect `structurally_empty` flag (SRC-04)
6. Assign `category_confidence` and `secondary_category`

**Stage 1 — Dimension scoring**
1. Score all 11 dimensions using L1–L3 signals
2. Apply structural emptiness gate to calorie density, glycemic, and fat quality dimensions (SRC-04)
3. Compute weighted dimension score

**Stage 2 — Guardrail evaluation (modified)**
1. Evaluate sugar caps with SC-class routing (SRC-02)
2. Evaluate HP patterns with NOVA gate (SRC-06)
3. Evaluate LOW_SATIETY rules with category gate (SRC-03)
4. Evaluate sodium cap with context flag (SRC-03)
5. All other guardrail rules: unchanged

**Stage 3 — Concern coordination** (unchanged)

**Stage 4 — Family budget clamp** (unchanged)

**Stage 5 — Cap application** (unchanged)

**Stage 6 — Relative penalty scaling (new — SRC-05)**
1. Check total coordinated penalties against relative budget
2. Scale penalties if relative cap is binding

**Stage 7 — Penalty application** (unchanged logic; scaled amounts from Stage 6)

**Stage 8 — Floor application (modified — SRC-01)**
1. Identify binding caps and classify as Class A or Class B
2. Apply full floor if no Class B caps bind
3. Apply physiological moderation minimum (60) if Class B caps bind and product is NOVA 1 single-ingredient
4. Apply reduced moderation minimum (50) if ISRAELI_RED_LABELS_2_PLUS fires on a NOVA 1 product

**Stage 9 — Confidence ceiling** (unchanged)

**Stage 10 — Context-limited post-processing (new — SRC-03)**
1. Annotate grade with context flag
2. Attach context note to output record

**Stage 11 — Category confidence output (new — SRC-07)**
1. Attach category confidence, delta, sensitivity, and flag to output record

---

## Updated Expected Qualitative Outcomes — 10 Workshop Products

The following updates the qualitative expectations using the resolutions above. Score ranges are indicative; exact values require calibrated threshold testing.

| # | Product | Prior outcome | Resolution(s) applied | Updated outcome | Change |
|---|---------|--------------|----------------------|-----------------|--------|
| 1 | Plain almonds | ~88, Grade A | None required | ~88, Grade A | Unchanged |
| 2 | Dates (whole dried) | Floor-cap conflict; unresolved | SRC-01, SRC-02 | SC-1 routing suspends HIGH_SUGAR cap. ISRAELI_RED_LABEL_1 noted but cap suspended (SC-1). No binding cap. NOVA 1 floor applies. Score ~75–80, Grade B | Resolved |
| 3 | Coconut oil | ~47 pre-floor, 28-point conflict | SRC-01, SRC-03, SRC-06 | LOW_SATIETY rules gated (cooking oil). HP gate (NOVA 1) suppresses HP_FAT_SODIUM. ISRAELI_RED_LABEL_1 sat fat fires → Class B cap → physio moderation minimum 60. Context-limited flag. Score ~60–65, Grade C* | Resolved |
| 4 | Brined olives | ~60 cap vs. 65 floor conflict | SRC-01, SRC-03, SRC-06 | HP_FAT_SODIUM suppressed (NOVA 1–2 HP gate). HIGH_SODIUM_700MG_PLUS → Class B cap, softened at 70% weight for brined context. Physio moderation minimum 60 applies. Context-limited flag. Score ~60–63, Grade C* | Resolved |
| 5 | Date-nut bar | Cap-masked category conflict; HP fires | SRC-02, SRC-06, SRC-07 | HP_FAT_SUGAR suppressed (NOVA 2). SC-2 routing: threshold raised to 40g; at ~45g sugar, HIGH_SUGAR still fires at softened level → cap ~60. Medium category confidence → 10% cap relaxation → effective cap ~66. Category delta simulation runs. Score ~55–65 range depending on category, with classification sensitivity surfaced | Significantly improved |
| 6 | Sugary granola bar | ~15–20, deep Grade E | SRC-05 | Pre-penalty score ~28. Relative penalty cap: max penalty = 28 × 0.50 = 14. Score: ~28 − 14 = 14 → absolute floor at 15. Score ~15–20, Grade E | Penalties bounded; grade unchanged |
| 7 | Coke Zero | ~42, Grade D (for wrong reasons) | SRC-04 | Structural emptiness gate fires. Calorie density dimension capped at 50 (not 95). NOVA 4 cap, SWEETENER cap, PROCESSING caps continue to govern. Pre-guardrail score drops from ~42 to ~30. Caps bind. Score ~38–42, Grade D/E | Reasoning improved; outcome similar |
| 8 | Diet chocolate mousse | ~45–55 range (structural emptiness paradox) | SRC-04 | Structural emptiness gate fires. Calorie density score capped at 50. NOVA 4 cap (60), SWEETENER cap (70), ADDITIVE_MARKERS cap (~55–65) continue. Score ~38–48, Grade D/E | Reasoning improved |
| 9 | Plain Greek yogurt | ~82–85, Grade B | None required | ~82–85, Grade B | Unchanged |
| 10 | Instant noodles | ~18, deep Grade E | SRC-05, SRC-06 | HP_FAT_SODIUM gated at NOVA 4 = 100% (no change for NOVA 4). Relative penalty budget: pre-penalty score ~33, max penalties = 33 × 0.50 = 16.5. Score: ~33 − 16 = 17 → absolute floor 15. Score ~18–22, Grade E | Penalties bounded; grade unchanged |

---

## Rules That Change

The following rules or behaviors are modified by this contract:

| Rule / Behavior | Change | Resolution |
|----------------|--------|-----------|
| HIGH_SUGAR_25G_PLUS | Suspended for SC-1; threshold raised to 40g for SC-2 | SRC-02 |
| HIGH_CAL_HIGH_SUGAR_SEVERE | Sugar context routing applied before firing | SRC-02 |
| HIGH_CAL_HIGH_SUGAR_MODERATE | Sugar context routing applied before firing | SRC-02 |
| ISRAELI_RED_LABEL_1 (sugar context) | Cap suspended for SC-1 single-ingredient NOVA 1; signal still noted in output | SRC-02 |
| HIGH_CAL_LOW_SATIETY_SEVERE | Gated: does not fire for cooking oil and pure fat products (whole_food_fat category) | SRC-03 |
| HIGH_CAL_LOW_SATIETY_SOFT | Gated: does not fire for cooking oil and pure fat products | SRC-03 |
| HIGH_SODIUM_700MG_PLUS | Applies at 70% cap weight for brined/pickled context-limited products | SRC-03 |
| HP_FAT_SUGAR_COMBO | Does not fire for NOVA 1–2 products; 50% weight for NOVA 3 | SRC-06 |
| HP_FAT_SODIUM_COMBO | Does not fire for NOVA 1–2 products; 50% weight for NOVA 3 | SRC-06 |
| HP_CRUNCH_SWEET_COMBO | Restricted to cereal category only | SRC-06 |
| Calorie density dimension | Score capped at 50 for structurally empty products | SRC-04 |
| Fat quality dimension | Returns neutral 50 when total fat < 0.5g/100g | SRC-04 |
| NOVA 1 floor (75) | Now conditional: applies fully only when no Class B cap fires; reduced to physio moderation minimum (60) when Class B cap fires and is not exempted | SRC-01 |
| Penalty total | Relative penalty cap added: penalties may not exceed 50% of pre-penalty score | SRC-05 |
| Category-specific cap thresholds | Raised 10% at medium category confidence | SRC-07 |
| Category-specific calorie density table | Relaxed 10% at medium confidence; default table substituted at low confidence | SRC-07 |

---

## Rules That Remain Unchanged

The following rules are not modified by this contract:

| Rule | Status |
|------|--------|
| SWEETENER_PRESENT (cap 70, independent) | Unchanged — architectural commitment |
| Trans fat veto (score = 0) | Unchanged — safety commitment |
| NOVA_PROXY_4_ULTRA_PROCESSED (cap 60) | Unchanged |
| ADDITIVE_MARKERS_3_PLUS (cap 65) | Unchanged |
| ADDITIVE_MARKERS_5_PLUS (cap 55) | Unchanged |
| NOVA_PROXY_3_PROCESSED (cap 75) | Unchanged |
| SNACK_BAR_HIGH_CAL (cap 70) | Unchanged |
| SNACK_BAR_HIGH_CAL_SUGAR (cap 60) | Unchanged |
| SNACK_BAR_RED_SUGAR_LABEL (cap 55) | Unchanged |
| ISRAELI_RED_LABELS_2_PLUS (cap 45) | Unchanged |
| ISRAELI_RED_LABEL_1 (sat fat context) | Unchanged as cap (SRC-01 modulates the floor interaction; the cap itself still fires) |
| LONG_INGREDIENT_LIST penalty (−4) | Unchanged |
| MULTIPLE_ADDED_SUGAR_MARKERS penalty (−5) | Unchanged |
| HIGH_CAL_HIGH_SUGAR_SOFT penalty (−5) | Unchanged (sugar context routing applies to the thresholds, not to this soft penalty — separate evaluation) |
| SEED_OIL_PRESENT penalty (−3) | Unchanged |
| Concern coordination logic | Unchanged — winner-takes-full, others scaled by supporting_evidence_factor |
| Family budget clamps (all families) | Unchanged — relative penalty cap (SRC-05) is applied on top of family clamps, not instead of them |
| Confidence ceilings (insufficient ≤ 50, low ≤ 70) | Unchanged |
| NOVA 1–2 whole food fat floor (65) | Unchanged as a floor target; subject to SRC-01 conditional application |

---

## Remaining Unresolved Contradictions

The following contradictions are documented but NOT resolved by this contract. They require additional design work or a deliberate decision to defer.

### UCON-01 — Date-nut bar sugar threshold at SC-2

After SC-2 routing raises the HIGH_SUGAR threshold to 40g, a date-nut bar at 45g sugar still triggers the softened cap. The product genuinely exists in a grey zone: concentrated whole-fruit sugar in a multi-ingredient bar. The SC-2 treatment reduces the severity of the cap but does not eliminate it. Whether a score of ~55–65 for a date-nut bar is analytically correct depends on a calibration decision (how much does concentrated whole-fruit sugar differ from added sugar in its physiological effect?) that cannot be made from architecture alone. This requires evidence review.

### UCON-02 — Fermented food NOVA classification ambiguity

Miso, kimchi, kefir, and sourdough bread have uncertain NOVA classifications (NOVA 2 vs. NOVA 3 depending on classification approach). The HP gate and the processing cap behavior change materially across this boundary. The architecture cannot distinguish "NOVA 3 because it is fermented" from "NOVA 3 because it contains additives." A fermentation marker at L3 is needed but not yet defined. This is noted in `beneficial_processing.md` as a future direction.

### UCON-03 — Grade suppression vs. user expectation for low-confidence categories

This contract specifies that low category confidence (< 0.50) should substitute the default category table and mark the grade with a double asterisk. The UI/UX implication — users seeing a ** grade for a product they expect to have a clear score — is not addressed. The contract defines the analytical behavior; the UI response is out of scope here and must be addressed in a separate UI specification.

### UCON-04 — Penalty-on-low-base interaction with family budget clamps

Two penalty-limiting mechanisms now coexist: family budget clamps (per family, absolute) and the relative penalty cap (total, proportional). The order of operations is defined in the score assembly sequence (Stage 6 after Stage 4), but edge cases exist: a product where family budget clamps alone produce a total penalty of 18, which the relative cap reduces to 14, which then gets re-distributed across families proportionally. The proportional redistribution rule within families after relative scaling is not specified. This requires implementation-phase clarification.

### UCON-05 — Structural emptiness gate does not cover medium-calorie engineered products

The structural emptiness gate requires calorie density < 80 kcal/100g. An engineered product at 90–120 kcal/100g with 1g protein, 0.5g fiber, and a full sweetener and additive system (e.g., a very light flavoured rice cake variant) does not trigger the gate. The gate captures the extreme emptiness cases but not the medium-density structural emptiness problem. This is acknowledged in `structural_emptiness_concept.md` and deferred to the positive architecture framework.

---

## Contract Metadata

**Resolutions defined:** 7  
**Rules modified:** 16  
**Rules unchanged:** 19  
**Unresolved contradictions documented:** 5  
**Source document:** validation/manual_trace_workshop_results.md  
**Supersedes:** Implicit floor-cap behavior in methodology.md (Section 7, Step 5)  
**Next required action:** Implement Stage 0 pre-scoring classification as the first engineering task in the scoring pipeline. All other resolutions depend on the evaluation_status and context_flag fields being populated before scoring runs.
