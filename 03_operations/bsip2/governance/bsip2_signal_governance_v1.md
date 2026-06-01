# BSIP2 Signal Governance Framework v1

**Document:** bsip2_signal_governance_v1.md
**Owner:** Chief Nutrition Officer
**Status:** ACTIVE — Governance Reference
**Created:** 2026-05-31
**Task:** TASK-045

---

## Purpose

This document defines the formal governance rules for BSIP2 signals. It establishes what signals exist, how they are classified, where they activate, how much influence they are permitted to exert, and how they interact with each other.

BSIP2 must remain interpretable. Every signal added without governance erodes the system's ability to explain a score. This framework is the mechanism that prevents rule accumulation.

---

## Section 1 — Signal Inventory

### 1.1 Nutrition Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-004 | Allulose Exemption | **PRODUCTION** | Allulose excluded from sugar scoring (0.4 kcal/g, zero glycemic load) |
| EV-005 | Polyol Laxative Threshold | **PRODUCTION** | −10 pts for 2+ polyol types; −15 pts for keto + polyols combo |
| EV-006 | Viscous vs Non-Viscous Fiber | **DEFERRED** | Distinguishes soluble viscous fiber (psyllium, beta-glucan) from bulk fiber |
| EV-007 | Intrinsic vs Isolated Fiber | **DEFERRED** | Distinguishes fiber naturally present in whole food from added/extracted fiber |
| EV-011 | Sodium-to-Potassium Ratio | **RESEARCH_ONLY** | Potassium data <10% declared on Israeli labels — insufficient coverage |
| EV-016 | Fortification Discount | **DEFERRED** | 30% discount on synthetic nutrient fortification contribution |
| EV-020 | Resistant Starch | **RESEARCH_ONLY** | Quantity not label-readable; detection limited to ingredient inference |
| BSIP2-064 | Plant Protein Hierarchy | **CANDIDATE** | Ranks protein source quality: whole legume > legume concentrate > isolated protein |

### 1.2 Processing Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-001 | Siga/MUP Classification | **DEFERRED** | MUP taxonomy classification; requires Hebrew ingredient dictionary |
| EV-002 | At-Risk Additive Count | **DEFERRED** | Counts at-risk additives against maintained regulatory list; depends on EV-001 |
| EV-009 | Intact Grain / Milling Disruption | **DEFERRED** | Detects grain processing state; prerequisite for cereal category launch |
| EV-010 | Extrusion Matrix Destruction | **DEFERRED** | Detects extruded matrix; requires calibration against matrix_integrity module |
| EV-018 | Reconstituted Matrix Flag | **DEFERRED** | No corpus impact until dairy categories launch |
| BSIP2-065 | Engineered Hyper-Palatability Flag | **CANDIDATE** | Detects fat + sugar + salt + texture engineering at bliss-point thresholds |

### 1.3 Matrix Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-008 | Liquid vs Solid Matrix Satiety | **RESEARCH_ONLY** | Already captured by beverage archetype's strict calorie thresholds |
| EV-014 | Hard Cheese Matrix Exception | **DEFERRED** | Exempts hard cheese from standard fat penalties; requires yellow cheese routing |
| BSIP2-061 | Water-to-Primary Ingredient Predominance | **CANDIDATE** | Flags water appearing before or displacing primary functional ingredient |
| BSIP2-063 | Fruit Matrix Quality | **CANDIDATE** | Evaluates whole fruit vs fruit concentrate vs flavouring hierarchy |
| BSIP2-066 | Hydrocolloid Synergy Detection | **CANDIDATE** | Detects multiple hydrocolloids combined for texture engineering |

### 1.4 Ingredient Quality Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-012 | Fat Ratio Model | **PRODUCTION** | Replaces absolute saturated fat with unsaturated-to-saturated ratio for products with fat ≥ 8g; rewards tahini and nuts; penalises palm/coconut oil |
| BSIP2-062 | Hummus Tahini Density | **CANDIDATE** | Scores tahini presence and proportion as a positive quality signal in hummus/dips |

### 1.5 Additives Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-003 | Emulsifier Tier Differentiation | **PRODUCTION** | Removes lecithin penalty; exempts gum arabic (prebiotic) from stabiliser count |
| EV-019 | High-Risk Emulsifier Flag | **PRODUCTION** | CMC, Polysorbate 80, and Carrageenan flagged at 2× additive weight |
| EV-013 | Hyper-Palatability / Bliss Point | **RESEARCH_ONLY** | Superseded by BSIP2-065; original EV-013 deferred for high false-positive risk |
| EV-017 | Sweetener-Induced Dysbiosis | **RESEARCH_ONLY** | High inter-individual variability; implement as disclosure flag only, never score deduction |
| BSIP2-066 | Hydrocolloid Synergy Detection | **CANDIDATE** | See Matrix Signals above; listed here due to additive mechanism |

### 1.6 Fermentation Signals

| Code | Signal Name | Status | Description |
|------|-------------|--------|-------------|
| EV-015 | Fermentation Bonus | **DEFERRED** | Cannot currently distinguish genuine sourdough from commercial yeast or added acidulants; vocabulary fix required before deployment |

### 1.7 Category-Specific Signals

The following signals are architecturally global but are restricted by routing to specific product categories. They are listed here because their governance requirements differ from universally applicable signals.

| Code | Signal Name | Restricted To |
|------|-------------|---------------|
| EV-009 | Intact Grain / Milling Disruption | Cereals, breads, whole grain products |
| EV-010 | Extrusion Matrix Destruction | Cereals, extruded snack bars |
| EV-014 | Hard Cheese Matrix Exception | Yellow cheese, hard/semi-hard cheese |
| EV-015 | Fermentation Bonus | Bread, yogurt, fermented spreads, kimchi, kefir |
| BSIP2-061 | Water-to-Primary Ingredient Predominance | Hummus, dips, spreads, sauces — NOT bread, cereals, beverages |
| BSIP2-062 | Hummus Tahini Density | Hummus, tahini-based dips — NOT general spreads |
| BSIP2-063 | Fruit Matrix Quality | Jams, fruit spreads, fruit yogurts, smoothie bases |

---

## Section 2 — Signal Classification

Every BSIP2 signal carries one of four classifications. Classification determines what review is required before deployment and what ongoing oversight applies.

| Classification | Meaning | Deployment Gate |
|----------------|---------|-----------------|
| **GLOBAL** | Applies across all product categories without routing restriction | Evidence review + CNO sign-off |
| **CATEGORY_SPECIFIC** | Applies only to defined activation categories; no-op elsewhere | Evidence review + category routing validation + CNO sign-off |
| **EXPERIMENTAL** | Under evaluation; may be piloted on limited category/corpus; not production | Pilot plan + impact measurement + CNO promotion decision |
| **RESEARCH_ONLY** | Insufficient data, high false-positive risk, or concept not yet operationalisable | No deployment path without formal CNO requalification |

### Full Classification Register

| Code | Signal Name | Classification |
|------|-------------|----------------|
| EV-003 | Emulsifier Tier Differentiation | GLOBAL |
| EV-004 | Allulose Exemption | GLOBAL |
| EV-005 | Polyol Laxative Threshold | GLOBAL |
| EV-012 | Fat Ratio Model | GLOBAL |
| EV-019 | High-Risk Emulsifier Flag | GLOBAL |
| EV-001 | Siga/MUP Classification | GLOBAL |
| EV-002 | At-Risk Additive Count | GLOBAL |
| EV-006 | Viscous vs Non-Viscous Fiber | GLOBAL |
| EV-007 | Intrinsic vs Isolated Fiber | GLOBAL |
| EV-016 | Fortification Discount | GLOBAL |
| EV-009 | Intact Grain / Milling Disruption | CATEGORY_SPECIFIC |
| EV-010 | Extrusion Matrix Destruction | CATEGORY_SPECIFIC |
| EV-014 | Hard Cheese Matrix Exception | CATEGORY_SPECIFIC |
| EV-015 | Fermentation Bonus | CATEGORY_SPECIFIC |
| EV-018 | Reconstituted Matrix Flag | CATEGORY_SPECIFIC |
| BSIP2-061 | Water-to-Primary Ingredient Predominance | EXPERIMENTAL |
| BSIP2-062 | Hummus Tahini Density | EXPERIMENTAL |
| BSIP2-063 | Fruit Matrix Quality | EXPERIMENTAL |
| BSIP2-064 | Plant Protein Hierarchy | EXPERIMENTAL |
| BSIP2-065 | Engineered Hyper-Palatability Flag | EXPERIMENTAL |
| BSIP2-066 | Hydrocolloid Synergy Detection | EXPERIMENTAL |
| EV-008 | Liquid vs Solid Matrix Satiety | RESEARCH_ONLY |
| EV-011 | Sodium-to-Potassium Ratio | RESEARCH_ONLY |
| EV-013 | Hyper-Palatability / Bliss Point (original) | RESEARCH_ONLY |
| EV-017 | Sweetener-Induced Dysbiosis | RESEARCH_ONLY |
| EV-020 | Resistant Starch | RESEARCH_ONLY |

---

## Section 3 — Category Routing Matrix

This matrix defines which product categories activate each signal. A signal that fires outside its defined scope is a routing error.

### BSIP2-061 — Water-to-Primary Ingredient Predominance

**Activates for:**
- Hummus
- Dips (bean-based, vegetable-based)
- Spreads (savoury, tahini-based)
- Sauces (dense, paste-based)

**Does NOT activate for:**
- Bread (water is a natural and expected primary ingredient)
- Cereals (water added during processing, not dilution)
- Beverages (water is the matrix by category definition)
- Soups (water content is the archetype)
- Fruit products (water release from whole fruit is not dilution)

**Rationale:** Water appearing before chickpeas in a hummus ingredient list is a dilution signal. The same observation in bread is architecturally meaningless.

---

### BSIP2-062 — Hummus Tahini Density

**Activates for:**
- Hummus
- Tahini-based dips
- Sesame-based spreads

**Does NOT activate for:**
- General spreads (avocado, bean dips without tahini tradition)
- Snack bars
- Any category where tahini is not a primary quality differentiator

**Rationale:** Tahini presence and proportion is a principal quality dimension in hummus specifically. Rewarding tahini density in unrelated categories would be category-inappropriate.

---

### BSIP2-063 — Fruit Matrix Quality

**Activates for:**
- Jams and fruit preserves
- Fruit spreads
- Fruit yogurts
- Smoothie bases and fruit compotes

**Does NOT activate for:**
- Savoury spreads
- Cereals with fruit pieces (fruit content is incidental, not the primary matrix)
- Snack bars (covered by ingredient list integrity, not matrix quality)
- Beverages (separate archetype rules apply)

---

### BSIP2-064 — Plant Protein Hierarchy

**Activates for:**
- All product categories

**Classification:** GLOBAL (once promoted from EXPERIMENTAL)

**Hierarchy tiers:**
1. Whole legume or intact seed protein (highest quality)
2. Legume concentrate (moderate quality)
3. Isolated plant protein (lowest quality — quantity rewarded by nutrient_density, source penalised by this signal)

---

### BSIP2-065 — Engineered Hyper-Palatability Flag

**Activates for:**
- Snack bars
- Sweet snacks
- Savoury snacks with engineered texture
- Ultra-processed ready meals

**Does NOT activate for:**
- Whole food products (NOVA 1–2 inference)
- Single-ingredient products
- Products where fat + sugar + salt combination is category-inherent (e.g., aged cheese)

**Trigger mechanism:** Nutritional composition thresholds only — NOT additive presence alone (to prevent double-counting with EV-019).

---

### BSIP2-066 — Hydrocolloid Synergy Detection

**Activates for:**
- Dips and spreads
- Sauces
- Dairy and dairy alternatives
- Snack bars

**Does NOT activate for:**
- Products where single hydrocolloid is declared and no synergistic partner is present
- Bread (leavening gums serve structural, not texture-engineering, function)

**Trigger:** ≥2 hydrocolloids from different functional classes present simultaneously. Single hydrocolloid does not trigger this signal (already handled by EV-019 individual penalty).

---

### Existing Signal Routing Summary

| Signal | Hummus | Snack Bar | Bread | Cereals | Yellow Cheese | Dairy/Yogurt | Beverages |
|--------|--------|-----------|-------|---------|----------------|--------------|-----------|
| EV-003 (Emulsifier Tier) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| EV-004 (Allulose) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| EV-005 (Polyol) | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| EV-012 (Fat Ratio) | ✓ | ✓ | — | — | ✓ | ✓ | — |
| EV-019 (High-Risk Emulsifier) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| EV-009 (Grain Milling) | — | — | ✓ | ✓ | — | — | — |
| EV-010 (Extrusion) | — | ✓ | — | ✓ | — | — | — |
| EV-014 (Hard Cheese Exception) | — | — | — | — | ✓ | — | — |
| EV-015 (Fermentation) | — | — | ✓ | — | — | ✓ | — |

---

## Section 4 — Influence Caps

No single signal should be able to determine a product's grade. The following caps define the maximum score impact each signal is permitted to exert, preventing any one observation from dominating the final score.

### 4.1 Hard Score Caps (Architecture-Level)

These caps are pre-applied to the final score regardless of dimension scoring.

| Cap | Trigger | Score Ceiling | Rationale |
|-----|---------|---------------|-----------|
| NOVA 3 Processing Cap | NOVA inference = 3 | 87 | Commercial processing inherently limits top-grade status |
| Additive Burden Cap | ≥3 distinct additive categories | 72 | Heavy additive burden is disqualifying for top grades |
| High Sodium Cap | Sodium ≥700 mg/100g | 60 | Regulatory-level sodium is a structural disqualifier |
| Structural Emptiness Cap | Fat <0.5g + low protein + low fiber + additives | 50–60 | No nutritional basis to score higher |
| NOVA 1 Floor | NOVA 1 inferred | 85 minimum | Unprocessed whole food cannot score below this floor |

### 4.2 Per-Signal Influence Caps (New Signals)

| Signal | Max Positive Impact | Max Negative Impact | Applies Within |
|--------|---------------------|---------------------|----------------|
| BSIP2-061 (Water Predominance) | — | −10 pts | whole_food_integrity dimension |
| BSIP2-062 (Tahini Density) | +8 pts | — | ingredient_quality dimension |
| BSIP2-063 (Fruit Matrix Quality) | +6 pts | −6 pts | matrix dimension |
| BSIP2-064 (Plant Protein Hierarchy) | +8 pts | −8 pts | protein_quality dimension |
| BSIP2-065 (Hyper-Palatability Flag) | — | −12 pts (binary) | post-cap penalty |
| BSIP2-066 (Hydrocolloid Synergy) | — | −8 pts | additive_quality dimension |

### 4.3 Post-Cap Penalties (Existing)

These fire after dimension scoring and hard caps. Listed here for completeness and to establish the penalty stack context for new signals.

| Penalty | Trigger | Impact |
|---------|---------|--------|
| SEED_OIL_PRESENT | Refined soybean / canola oil detected | −3 pts |
| LONG_INGREDIENT_LIST | >12 ingredients | −4 pts |
| MULTIPLE_ADDED_SUGAR | ≥2 sugar sources | −5 pts |
| HIGH_CAL_LOW_SATIETY | High kcal + low protein + low fiber | −6 pts |

### 4.4 Stacking Rule

The combined post-cap penalty burden shall not exceed −20 pts in total, regardless of how many penalty signals fire. If penalties would exceed this ceiling, they are applied in descending impact order until the −20 limit is reached. This prevents penalty compounding from creating scores that are not explainable by any single dominant factor.

---

## Section 5 — Interaction Review

### 5.1 Fat Quality vs Tahini Density (EV-012 vs BSIP2-062)

**Nature:** Potential conflict — EV-012 evaluates fat composition ratios; BSIP2-062 rewards tahini presence.

**Risk:** Tahini contains ~15–20% saturated fatty acids (natural seed fat). If fat data is restored after TASK-039 scraper fix, the fat_quality dimension could penalise tahini-dense products for elevated SFA fractions, directly undermining the BSIP2-062 reward.

**Resolution:** EV-012's fat ratio model was explicitly designed to protect whole-food fats (tahini, nuts, seeds). The unsaturated-to-saturated ratio at these natural SFA levels should yield a net positive signal. **Before BSIP2-062 is deployed to production, validate this interaction against the corrected fat dataset.** Flag as a required co-validation step.

**Status:** Latent — blocked until TASK-039 fat data correction.

---

### 5.2 Matrix Quality vs Water Dilution (BSIP2-063 vs BSIP2-061)

**Nature:** False positive risk — in fruit-based products, water is a natural byproduct of whole-fruit processing, not a dilution indicator.

**Risk:** BSIP2-061 (Water-to-Primary Ingredient Predominance) firing on a jam containing real whole fruit where water releases during cooking would penalise quality products.

**Resolution:** BSIP2-061 must carry an exclusion rule: **if the product is routed to the fruit matrix category, BSIP2-061 does not fire.** The two signals are mutually exclusive by routing. This is an activation gate, not a scoring interaction.

**Status:** Must be written into routing rules before either signal enters pilot.

---

### 5.3 Fermentation Bonus vs Acidification Penalties (EV-015)

**Nature:** Double-counting — a product acidified with lactic acid or citric acid might trigger EV-015 (Fermentation Bonus) while simultaneously receiving regulatory_quality penalties for acidulant additives.

**Risk:** Net effect could be score inflation (bonus fires) and score deflation (penalty fires) for the same underlying chemical signature, making the score unexplainable.

**Resolution:** EV-015 must not be deployed until the vocabulary distinguishes:
1. `genuine_fermentation` — sourdough starter (מחמצת), live cultures declared
2. `commercial_yeast` — שמרים, rapid-rise yeast
3. `acidulant_addition` — citric acid, lactic acid, acetic acid as flavour/preservative

Only `genuine_fermentation` triggers the bonus. The other two fire no bonus. This is already identified as the Sprint 2 prerequisite.

**Status:** Blocking dependency confirmed. EV-015 is correctly DEFERRED.

---

### 5.4 Hydrocolloid Synergy vs Emulsifier Tier (BSIP2-066 vs EV-003/EV-019)

**Nature:** Double-counting — EV-019 already applies 2× weight to CMC, Polysorbate 80, and Carrageenan individually. BSIP2-066 proposes an additional penalty when multiple hydrocolloids appear together.

**Risk:** A product containing CMC + xanthan gum would receive EV-019's double-weight penalty on CMC plus a BSIP2-066 synergy penalty. The CMC is penalised twice for the same presence.

**Resolution:** BSIP2-066 must operate on the **net additive roster after EV-003/EV-019 classification** and may only add a synergy penalty for hydrocolloid combinations that are not already individually penalised at double weight. In practice: the synergy flag fires only when ≥2 hydrocolloids from the non-Tier-1 list appear together. It does not re-penalise any additive that EV-019 has already double-weighted.

**Status:** Interaction rule must be written into BSIP2-066 spec before pilot.

---

### 5.5 Plant Protein Hierarchy vs Nutrient Density Bonus (BSIP2-064 vs existing protein_quality)

**Nature:** Intentional tension — nutrient_density rewards protein quantity; BSIP2-064 penalises isolated protein source. The combination is the intended signal (high quantity, poor source = protein-enriched product that looks nutritious but is reconstructed).

**Risk:** The penalty from BSIP2-064 must be large enough to meaningfully reduce the score despite a large nutrient_density bonus. If the protein_quality dimension (10% weight) absorbs the BSIP2-064 penalty but nutrient_density (15% weight) provides a larger offsetting bonus, isolated-protein products may still rank above whole-food-protein products.

**Resolution:** The net score gap between a whole-legume protein product and an isolated-protein product with equal declared protein content must be validated during pilot. A minimum separation of 5 score points is the target. If calibration cannot achieve this, revisit the dimension weighting before production promotion.

**Status:** Calibration target defined. Validate during BSIP2-064 pilot.

---

### 5.6 Engineered Hyper-Palatability vs Additive Tier (BSIP2-065 vs EV-003/EV-019)

**Nature:** Mechanism overlap — BSIP2-065 targets engineered palatability via nutritional macro composition; EV-019 targets specific texture-engineering additives. Products engineered for hyper-palatability will often have both.

**Risk:** If BSIP2-065 fires on additive presence rather than compositional thresholds, it becomes a redundant re-expression of EV-019 with a larger penalty.

**Resolution:** BSIP2-065 must fire **exclusively on nutritional composition signals** — the fat/sugar/salt macro combination at bliss-point thresholds — and must be explicitly prohibited from using additive presence as a trigger. The additive dimension is EV-019's domain. Clear trigger separation prevents overlap.

**Status:** Trigger specification must define this boundary before any pilot.

---

### 5.7 Fiber Triple-Counting (Architecture-Level Issue)

**Nature:** Collinearity — fiber currently contributes to three dimensions simultaneously: nutrient_density (15% weight), glycemic_quality (12%), and satiety_support (6%). Total potential weight on a single nutrient: 33%.

**Risk:** Fiber-enriched products (with added inulin, polydextrose, or declared fiber) are structurally over-rewarded. EV-007 (Intrinsic vs Isolated Fiber) is designed to correct this when deployed, but until then the triple-count remains.

**Resolution:** This is a CNO architectural decision, not solvable by signal governance alone. Log as a pending ruling. EV-007 deployment is the primary mitigation path.

**Status:** Open — pending CNO ruling.

---

## Section 6 — New Signal Recommendations (BSIP2-061 to BSIP2-066)

### 6.1 Recommendation Summary

| Signal | Recommendation | Rationale |
|--------|----------------|-----------|
| BSIP2-062 Hummus Tahini Density | **Implement Now** | Directly addresses FM-4 (traditional quality hummus capped at B despite superior composition). High corpus relevance, bounded scope, clear measurement |
| BSIP2-061 Water-to-Primary Ingredient Predominance | **Pilot First** | Valid dilution signal with routing complexity. Pilot on hummus/dips only; validate no false positives in fruit-adjacent categories before widening |
| BSIP2-064 Plant Protein Hierarchy | **Pilot First** | Fills a confirmed gap (protein source not currently distinguished). Requires calibration against nutrient_density interaction before production |
| BSIP2-066 Hydrocolloid Synergy Detection | **Pilot First** | Meaningful signal for texture engineering detection. Requires interaction rules with EV-019 to be written before pilot launch to prevent double-counting |
| BSIP2-063 Fruit Matrix Quality | **Research Further** | No active fruit product corpus. Cannot calibrate or validate without data. Revisit at fruit category launch |
| BSIP2-065 Engineered Hyper-Palatability Flag | **Research Further** | Previously deferred as EV-013 for high false-positive risk. The core concern remains: thresholds are product-specific and corpus-dependent. Compositional trigger boundaries must be defined and validated before any pilot |

### 6.2 Output Table

| Signal | Classification | Activation Scope | Expected Coverage | Implementation Priority |
|--------|----------------|------------------|--------------------|------------------------|
| BSIP2-061 Water-to-Primary Ingredient Predominance | EXPERIMENTAL | Hummus, dips, spreads, sauces | Medium — fires when water is listed before primary functional ingredient | Pilot First — Sprint 3 |
| BSIP2-062 Hummus Tahini Density | EXPERIMENTAL → CATEGORY_SPECIFIC | Hummus, tahini-based dips | High — tahini presence is a primary hummus quality marker; 50–70% of hummus corpus expected to be affected | Implement Now — Sprint 2 |
| BSIP2-063 Fruit Matrix Quality | EXPERIMENTAL | Jams, fruit spreads, fruit yogurts | Low currently — no active fruit corpus | Research Further — Wave 3+ |
| BSIP2-064 Plant Protein Hierarchy | EXPERIMENTAL → GLOBAL | All categories | Medium — fires when protein source is detectable from ingredient list | Pilot First — Sprint 4 |
| BSIP2-065 Engineered Hyper-Palatability Flag | EXPERIMENTAL | Snack bars, sweet/savoury snacks, UPF | Medium-low — fires only at confirmed bliss-point threshold combinations | Research Further — Wave 3+ |
| BSIP2-066 Hydrocolloid Synergy Detection | EXPERIMENTAL → CATEGORY_SPECIFIC | Dips, spreads, sauces, dairy alternatives | Low-medium — fires only on multi-hydrocolloid combinations | Pilot First — Sprint 4 |

---

## Section 7 — Governance Rules

### 7.1 Signal Lifecycle

Every signal must pass through defined lifecycle stages. Skipping a stage requires explicit CNO authorisation.

```
RESEARCH_ONLY → EXPERIMENTAL → CATEGORY_SPECIFIC or GLOBAL → PRODUCTION
```

A signal may be demoted at any lifecycle stage if evidence quality deteriorates or corpus impact is unexplained.

### 7.2 Promotion Gates

**EXPERIMENTAL → CATEGORY_SPECIFIC or GLOBAL:**
- Evidence document filed in evidence_registry
- Pilot results showing expected directionality and bounded false-positive rate
- Interaction review against all current PRODUCTION signals
- CNO sign-off

**CATEGORY_SPECIFIC or GLOBAL → PRODUCTION:**
- Full corpus run completed
- Score distribution reviewed against authoritative baseline
- No unresolved interactions flagged in Section 5
- CNO sign-off

### 7.3 Signal Limit

The total number of simultaneously active PRODUCTION signals shall not exceed **20**. When this limit is approached, the CNO must retire or merge at least one existing signal before a new signal is promoted to PRODUCTION.

Current PRODUCTION signal count: **5** (EV-003, EV-004, EV-005, EV-012, EV-019)
Headroom remaining: **15**

### 7.4 Interpretability Requirement

For every PRODUCTION signal, a one-sentence plain-language explanation must exist that describes why the signal affects a product's score. If this explanation cannot be written clearly and without qualification, the signal is not ready for production.

Example (EV-019): "Products containing CMC, Polysorbate 80, or Carrageenan receive a higher additive burden score because these emulsifiers are associated with gut microbiome disruption at typical consumption levels."

### 7.5 Interaction Review Requirement

Any new signal proposed for PRODUCTION must undergo a documented interaction review against all existing PRODUCTION signals before deployment. The review must address every conflict identified in Section 5 that is relevant to the new signal.

### 7.6 Scoring Stability Test

Before any new PRODUCTION signal is activated, a full corpus run must be executed against the authoritative baseline (currently run_hummus_002 for hummus). Rank shifts greater than 5 positions for more than 10% of products require CNO review before deployment proceeds.

---

## Appendix A — Signals Requiring CNO Rulings (Open Items)

The following architectural questions are blocking signal promotion and are not resolvable within the governance framework alone. They require CNO decisions.

| Item | Question | Blocked Signals |
|------|----------|-----------------|
| Nutrient Density Breakpoints | Legume-based spreads avg 27.5 on nutrient_density — is this the intended range? | BSIP2-062, BSIP2-064 |
| Protein Source Distinction | Should the engine distinguish chickpea protein from isolated chickpea protein? | BSIP2-064 |
| Raising Agent Classification | Should sodium bicarbonate be excluded from additive_quality in sauce_spread archetype? | Affects FM-2 and hummus baseline |
| NOVA 3 Cap at 87 | Is 87 the correct ceiling for NOVA 3 commercial products? | FM-4: traditional quality hummus capped at B, not A |
| Fiber Triple-Count | Should fiber contribution be consolidated to one dimension? | EV-006, EV-007 |
| Fat Data Correction | Scraper returns SFA in TFA field for 58/69 hummus products — requires TASK-039 fix before EV-012 / BSIP2-062 interaction can be validated | EV-012, BSIP2-062 |

---

## Appendix B — Recommended Implementation Order

1. **Immediately:** BSIP2-062 Hummus Tahini Density — sprint planning for Sprint 2
2. **Sprint 2:** EV-015 Fermentation Bonus vocabulary fix (sourdough vs yeast vs acidulant split)
3. **Sprint 3:** BSIP2-061 Water-to-Primary Ingredient Predominance pilot (hummus/dips only)
4. **Sprint 3:** EV-006 Viscous vs Non-Viscous Fiber (vocabulary build)
5. **Sprint 3:** EV-007 Intrinsic vs Isolated Fiber (vocabulary build)
6. **Sprint 4:** BSIP2-064 Plant Protein Hierarchy pilot
7. **Sprint 4:** BSIP2-066 Hydrocolloid Synergy Detection pilot (with EV-019 interaction rules)
8. **Wave 2:** EV-001 / EV-002 MUP taxonomy (Yogurt/Milk category launch prerequisite)
9. **Wave 2:** EV-009 / EV-010 Grain processing (Cereal category launch prerequisite)
10. **Wave 3+:** BSIP2-063 Fruit Matrix Quality (fruit category launch)
11. **Wave 3+:** BSIP2-065 Engineered Hyper-Palatability (after threshold calibration research)

---

*This document is the authoritative governance reference for BSIP2. Changes to signal classification, influence caps, or interaction rules require CNO approval and a version increment.*
