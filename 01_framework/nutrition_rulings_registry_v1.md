# Nutrition Rulings Registry — v1

**Document type:** Authoritative registry of established Bari nutrition decisions  
**Scope:** BSIP2 scoring philosophy, category interpretation, signal methodology, and structural food rulings  
**Status:** Active  
**Last compiled:** 2026-05-30  
**Compiled by:** Chief Nutrition Officer

> This registry documents decisions already made. It does not create new rulings, revisit scores, or propose changes.

---

## Index

| ID | Subject | Status |
|----|---------|--------|
| [NR-001](#nr-001) | Milk Canonical Source | Active |
| [NR-002](#nr-002) | Snack Bar Health-Halo Ceiling | Active |
| [NR-003](#nr-003) | NOVA 4 Maximum Grade | Active |
| [NR-004](#nr-004) | Bread Fermentation Classification | Active |
| [NR-005](#nr-005) | Bread Fiber Source Evaluation | Active |
| [NR-006](#nr-006) | Fruit Juice Concentrate = Added Sugar | Active |
| [NR-007](#nr-007) | Carbohydrate Quality Proxy | Active |
| [NR-008](#nr-008) | NOVA 1 Single-Ingredient Floor | Active (v2 recalibrated) |
| [NR-009](#nr-009) | Whole-Food Fat Floor | Active (v2 recalibrated) |
| [NR-010](#nr-010) | Trans Fat Veto | Active |
| [NR-011](#nr-011) | Non-Nutritive Sweetener Cap | Active |
| [NR-012](#nr-012) | Israeli Red Label Thresholds | Active |
| [NR-013](#nr-013) | Concern Non-Duplication | Active |
| [NR-014](#nr-014) | Fortification Non-Credit | Active |
| [NR-015](#nr-015) | Fermentation Direct Bonus | Active |
| [NR-016](#nr-016) | Category-Relative Evaluation | Active |
| [NR-017](#nr-017) | Processing Principle | Active |
| [NR-018](#nr-018) | Grade Thresholds (v2 Recalibration) | Active — supersedes v1 |
| [NR-019](#nr-019) | Snack Bar NOVA 4 Ceiling | Active |
| [NR-020](#nr-020) | No Imputation Policy | Active |

---

## Rulings

---

### NR-001

**Subject:** Milk Canonical Source  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Whole cow's milk (single-ingredient, no additives) is the structural benchmark for the milk and alternatives comparison category. Its elevated score relative to plant-based alternatives is not a category bias — it reflects the structural fact that whole milk has a minimal ingredient list, no stabilization or emulsification systems, and requires no industrial reconstruction process.

**Rationale:**  
The milk analysis found that whole cow's milk achieved the highest score in the comparison not because of ideology or category preference, but because structural simplicity is a genuine analytical differentiator. Plant-based alternatives start from a simpler raw ingredient (oat grain, almond, soy bean) but arrive on shelf having undergone multiple industrial steps: separation, isolation, emulsification, stabilization, flavor correction, and fortification. Each step increases reconstruction depth and engineering intensity. A product requiring more steps to reach its shelf state scores lower on processing quality and whole-food integrity — this is analytically consistent, not a bias toward dairy.

The editorial copy makes this explicit: "Bari's algorithm does not reward ideology, trends, or categories — it examines the actual structure of the food."

**References:**  
- `milk-editorial-content.ts` (editorial intro paragraphs)  
- `milk-product-insights.ts` (barcode 7290000051352)  
- `methodology.md` §Category awareness

---

### NR-002

**Subject:** Snack Bar Health-Halo Ceiling  
**Date established:** Pre-2026-05-30 (HTC-01 in cap taxonomy)  
**Status:** Active

**Decision:**  
No snack bar (category: `snack_bar_granola`) with ≥ 430 kcal/100g can exceed a final score of 70, regardless of other positive signals. This cap is designated HTC-01 (Heuristic Temporary Cap 01) in the cap taxonomy. The practical result is that no snack bar can achieve grade A.

A secondary cap: snack bars with ≥ 470 kcal/100g AND ≥ 15g sugar are additionally capped at 60 (HTC-03).

**Rationale:**  
The snack bar category carries the strongest health-halo risk of any category in scope. Products are routinely marketed as nutritious, clean, or fitness-appropriate while delivering calorie densities approaching confectionery. The ceiling at 70 is a policy decision: a snack bar at or above confectionery calorie density cannot receive a "good" grade — this would validate the health-halo framing that the analytical system is specifically designed to expose.

The 70-ceiling is acknowledged to be heuristic. It is a candidate for eventual replacement by a steeper continuous calorie-penalty curve that achieves the same effect without a hard cliff. The cliff is a known gaming surface (reformulating from 431 kcal to 429 kcal produces no meaningful nutritional change but escapes the cap).

**References:**  
- `constants.py` (`CALORIE_CAPS`, `SNACK_BAR_HIGH_CAL`)  
- `cap_taxonomy.md` (HTC-01, HTC-02, HTC-03)  
- `category_analysis.md` (snack_bar_granola section)  
- `snack-editorial-content.ts` ("הציון הגבוה ביותר — 70/B")

---

### NR-003

**Subject:** NOVA 4 Maximum Grade  
**Date established:** Pre-2026-05-30 (BRC-01); threshold updated in v2 recalibration  
**Status:** Active

**Decision:**  
Products classified as NOVA 4 (ultra-processed) are capped at a final score of 68. This places the maximum possible grade for any NOVA 4 product at the upper boundary of grade B in the v2 threshold system, but in practice — given that NOVA 4 products also frequently trigger sugar, additive, or calorie caps — the effective ceiling for most NOVA 4 products is grade D.

The consumer-facing framing is explicit: NOVA 4 is a score ceiling, not a category of "bad foods."

**Rationale:**  
Ultra-processed foods as a class are associated at population level with poorer health outcomes (NOVA framework, epidemiological evidence base). The cap reflects a structural assessment: a product whose food architecture is characteristic of ultra-processing cannot receive a high grade on a system that evaluates nutritional architecture. The NOVA inference is a proxy classification — it carries classification uncertainty — and the cap is acknowledged as a behavioral-risk cap that eventually should become confidence-weighted (i.e., NOVA 4 with high classification confidence → hard cap; NOVA 4 with low confidence → gradient penalty proportional to confidence).

The cap value was adjusted from 60 to 68 in the v2 recalibration to prevent over-penalization of borderline NOVA 3/4 products and to smooth the transition between processing levels.

**References:**  
- `constants.py` (`PROCESSING_CAPS`, `NOVA_PROXY_4_ULTRA_PROCESSED`)  
- `cap_taxonomy.md` (BRC-01)  
- `snack-editorial-content.ts` ("NOVA4 הוא תקרת ציון — לא מדד 'רע'")

---

### NR-004

**Subject:** Bread Fermentation Classification  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Bread products containing the word "sourdough" (מחמצת) in their name are evaluated by verifying the presence and position of fermentation markers in the ingredient list. Three fermentation tiers are recognized:

| Tier | Definition | Score effect |
|------|-----------|-------------|
| Traditional | Lactic fermentation identified in ingredients; starter/culture appears before commercial yeast | Full fermentation bonus; average A |
| Mixed | Both sourdough culture and commercial yeast present; culture is present but not dominant | Partial credit; average B |
| Flavor-only | Commercial yeast is the leavening agent; sourdough culture appears at low quantity for flavor, or apple cider vinegar is used as a proxy | No fermentation credit; average B–C |

Products with "sourdough" in the name but commercial yeast before the starter in the ingredient list are classified as "sourdough in name, yeast in ingredients" — a named mislabeling pattern documented in the bread analysis.

**Rationale:**  
The word "sourdough" carries 31.6 points of score difference in the analysis between a genuinely fermented product and a product using sourdough as a flavoring element. The difference is real: genuine long fermentation (24–48 hours) reduces phytates, pre-digests gluten, lowers glycemic response, and produces flavor complexity that cannot be industrially replicated. Using the name without the process is a health-halo claim. The classification system is designed to surface this gap.

**References:**  
- `bread-editorial-content.ts` (fermentation zones and lookalikes)  
- `bakery_semantics.py` (fermentation marker detection)  
- `constants.py` (`FERMENTATION_DIRECT_BONUS = 8`)

---

### NR-005

**Subject:** Bread Fiber Source Evaluation  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
When evaluating bread products, fiber quantity is not sufficient on its own — fiber source determines whether the fiber signal is counted as a whole-grain structural positive or as an isolated additive. Fiber derived from the grain matrix (whole grain rye, whole wheat) contributes positively to processing quality, matrix integrity, and satiety scores. Fiber added as isolated compounds (inulin, psyllium, isolated beta-glucan, methylcellulose) contributes to fiber quantity on the nutrition panel but is treated as an additive, not a whole-grain signal.

**Rationale:**  
Two products can show identical fiber content on the nutrition panel while being structurally different. A product with 10g fiber from whole rye has retained the original grain matrix; a product with 12g fiber from isolated inulin added to a white flour base has added a functional ingredient to a structurally inferior base. The scores reflect this: the white flour + isolated fiber product (C: 50.1) scores substantially below the whole-rye product (A: 84.8) despite having more fiber per gram.

The distinction matters for consumer communication: "rich in fiber" on the pack is not analytically equivalent across fiber sources.

**References:**  
- `bread-editorial-content.ts` (lookalike: "fiber source")  
- `signal_system.md` (`whole_grain` vs. fiber additive markers)  
- `bakery_semantics.py`

---

### NR-006

**Subject:** Fruit Juice Concentrate = Added Sugar  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Fruit juice concentrate in an ingredient list is treated as added sugar for scoring purposes, not as a whole-food component. It triggers the `added_sugar` marker and is included in the sugar source count. This applies regardless of whether the concentrate is marketed as "natural sweetener," "fruit sugar," or as a substitute for refined sugar.

**Rationale:**  
Concentration is beneficial when it is water removal from whole food (dried fruit, tahini). It becomes a fragmentation step when specific fractions are separated and reconcentrated for use as a sweetening agent. Fruit juice concentrate is the latter: the fiber, cell matrix, and phytochemicals of the original fruit are removed; the resulting concentrated liquid is a refined sugar equivalent for glycemic and structural purposes. Treating it as a whole-food component would credit a product for a health-halo ingredient that delivers the same glycemic burden as cane sugar.

**References:**  
- `beneficial_processing.md` (concentration/fragmentation distinction)  
- `signal_system.md` (Group 2 — `added_sugar`, `date_or_fruit_paste`)

---

### NR-007

**Subject:** Carbohydrate Quality Proxy  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
The sugar-to-carbohydrate ratio (sugars_g / carbohydrates_g) is used as a derived signal for glycemic quality assessment. A high ratio indicates that most carbohydrates are simple sugars; a low ratio indicates complex carbohydrates or fiber retention. This ratio is evaluated alongside absolute sugar quantity, not instead of it.

Additionally, fiber-to-carbohydrate ratio is used in the hyper-palatability engine to assess whether high-carbohydrate products have compensating fiber structures.

Total carbohydrates are not penalized as a category — only the sugar concentration within them and the processing signals that accompany them. A high-carbohydrate product with high whole-grain content and low sugar scores differently from a high-carbohydrate product with high refined flour and high glucose syrup.

**Rationale:**  
Carbohydrate quality cannot be evaluated by total carbohydrate quantity alone. Two products at 60g carbohydrate/100g may have radically different structural profiles: one with 5g sugar and 10g fiber from whole grain, another with 45g sugar and 1g fiber from refined flour. The ratio-based approach preserves category awareness while flagging the structurally poor carbohydrate profiles.

**References:**  
- `signal_system.md` (Group 1, derived signals)  
- `constants.py` (HP engine thresholds)  
- `methodology.md` (Glycemic Quality dimension)

---

### NR-008

**Subject:** NOVA 1 Single-Ingredient Floor  
**Date established:** Original: pre-2026; v2 recalibration: raised from 75 to 85  
**Status:** Active (v2 recalibrated)

**Decision:**  
A product classified as NOVA 1 (unprocessed or minimally processed whole food) AND identified as single-ingredient receives a minimum final score of 85, regardless of what other analytical rules produce. This floor cannot be overridden by dimension scores but can be reduced by explicit regulatory exceptions (confidence ceilings do not override floors; red label caps can interact depending on the concern family).

**Rationale:**  
Many analytical penalties in BSIP2 are calibrated for engineered products. A single-ingredient whole food — plain walnuts, plain oats, plain tahini — may appear analytically concerning on calorie density or fat quality dimensions because those dimensions were calibrated against a population of processed products. Applying full penalties to a whole food produces analytically absurd results: plain walnuts scoring D is not a meaningful nutritional conclusion. The floor enforces the system's commitment to contextual evaluation: it cannot produce a result that is analytically incoherent for the product type.

The floor was raised from 75 to 85 in the v2 recalibration to align with the updated grade threshold system where 80+ = grade A.

**References:**  
- `constants.py` (`NOVA1_SINGLE_FLOOR = 85`)  
- `batch_run_milk_004.py` (v2 recalibration notes)  
- `category_analysis.md` (whole-food protection section)

---

### NR-009

**Subject:** Whole-Food Fat Floor  
**Date established:** Original: pre-2026; v2 recalibration: raised from 65 to 70  
**Status:** Active (v2 recalibrated)

**Decision:**  
Products classified as NOVA 1–2 AND in the `whole_food_fat` category (nut butters, tahini, seeds, avocado-based products) receive a minimum final score of 70. This applies even when fat quality, calorie density, or satiety dimension scores would otherwise pull the product lower.

**Rationale:**  
Whole-food fat products are naturally calorie-dense (600–900 kcal/100g is normal for nut butters and seeds) and high in fat. The calorie density and fat quality dimensions are calibrated for processed products; their thresholds would incorrectly penalize products whose nutritional characteristics are intrinsic to the food. A plain almond butter at 600 kcal/100g is not calorie-concerning in the same sense as an engineered 600 kcal/100g bar.

The floor was raised from 65 to 70 in the v2 recalibration to prevent grade C results for high-quality whole-food fats.

**References:**  
- `constants.py` (`WHOLE_FOOD_FAT_FLOOR = 70`)  
- `batch_run_milk_004.py` (v2 recalibration notes)  
- `category_analysis.md` (whole_food_fat thresholds and design rationale)

---

### NR-010

**Subject:** Trans Fat Veto  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
A product with > 1.0g/100g industrially produced trans fat receives a final score of 0 (full veto). This is not a cap — it overrides all other scores, floors, and caps. The score of 0 cannot be raised by any other rule in the system.

Two sub-threshold flags exist:
- 0.5–1.0g/100g: `high_trans_fat_concern` flag (no veto, but heavy penalty)
- 0.2–0.5g/100g: `trans_fat_present` flag

**Rationale:**  
Industrially produced trans fats have no safe level of consumption at a population level — this is scientific consensus with WHO and regulatory confirmation. A veto, not a cap, is the appropriate analytical response: no grade above E can be justified for a product that contains a compound with no safe intake level. This is BSIP2's only full veto rule and it is SC-02 (Safety Cap 02) in the cap taxonomy — an architectural commitment.

**References:**  
- `constants.py` (`TRANS_FAT_VETO_THRESHOLD = 1.0`)  
- `cap_taxonomy.md` (SC-02)

---

### NR-011

**Subject:** Non-Nutritive Sweetener Cap  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Any product containing a non-nutritive sweetener — synthetic or natural — is capped at a final score of 70. This prevents such products from reaching grade A. The cap is uniform across sweetener tiers; the tier determines an additional penalty beyond the cap but does not raise the ceiling.

| Tier | Examples | Cap | Penalty |
|------|----------|-----|---------|
| A (fermentation-derived/natural) | Stevia, monkfruit, thaumatin | 75 → 70 (uniform cap) | −8 |
| B (sugar alcohols) | Erythritol, xylitol, sorbitol, maltitol | 75 → 70 (uniform cap) | −10 |
| C (synthetic) | Aspartame, sucralose, acesulfame-K, saccharin | 70 | −15 |

> Note: The constants file shows tier-differentiated caps (75/73/70). The cap taxonomy documents the uniform architectural principle as a cap at 70 for any sweetener-present product. The worst tier present in a product applies.

**Rationale:**  
Non-nutritive sweetener substitution is not a nutritional quality improvement. A product that replaces sugar with sweeteners has not improved its food structure — it has modified a palatability signal without changing the underlying composition problem. Allowing such products to score grade A would imply that sweetener-formulated products are preferable to sugar-containing equivalents on a food quality basis. This is not analytically supportable.

The cap is deliberately uniform at the architectural level — distinguishing the burden of one sweetener vs. three sweeteners is deferred to a later calibration phase.

**References:**  
- `constants.py` (`SWEETENER_CAP_A/B/C`, `SWEETENER_PENALTY_A/B/C`)  
- `cap_taxonomy.md` (SC-01)

---

### NR-012

**Subject:** Israeli Red Label Thresholds  
**Date established:** Pre-2026-05-30 (statutory; embedded as structural inputs)  
**Status:** Active

**Decision:**  
Israeli Ministry of Health front-of-pack red label thresholds are embedded as structural analytical inputs, not merely as display flags. Exceeding a threshold triggers guardrail caps:

| Nutrient | Threshold | Guardrail consequence |
|----------|----------|-----------------------|
| Sugar | 17.5g/100g | Score cap at 55 (single label); 45 (2+ labels) |
| Saturated fat | 5.0g/100g | Score cap at 55 |
| Sodium | 600mg/100g | Structural flag; sodium cap (700mg+) is stricter |

A product with 2+ red labels is capped at 45 (grade E) regardless of other scores.

**Rationale:**  
The regulatory thresholds represent a government determination that a structural nutritional concern exists. The analytical system respects this determination by treating the label as a structural input rather than a display element. A product that has triggered a regulatory warning process for sugar or saturated fat cannot analytically receive a grade above D–E on a system whose purpose is to assess structural food quality.

The sodium threshold interaction is complex: the Israeli red label fires at 600mg/100g but the BSIP2 guardrail cap fires at 700mg/100g. Both thresholds coexist; the more restrictive applies when both fire.

**References:**  
- `constants.py` (`RED_LABEL_THRESHOLDS`)  
- `cap_taxonomy.md` (SC-03, SMC-06, SMC-07)  
- `signal_system.md` (Group 3 — Regulatory flags)

---

### NR-013

**Subject:** Concern Non-Duplication  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
The same underlying nutritional concern can apply only once to the final score, regardless of how many analytical rules identify it. A product with high sugar will trigger multiple sugar-related rules; the concern coordination layer selects the primary signal and demotes all other same-family signals to reduced weight. Per-family budget caps prevent cumulative over-penalization.

Concern families and budgets:
| Family | Budget |
|--------|--------|
| Sugar load | 10 points |
| Sodium load | 8 points |
| Calorie load | 8 points |
| Processing load | 12 points |
| Fat quality | 8 points |
| Hyper-palatability | 12 points |

**Rationale:**  
Without coordination, the same root issue (e.g., high sugar) would be counted by the glycemic quality dimension penalty, the additive quality dimension, the hyper-palatability engine, and multiple guardrail caps — each at partial weight, but cumulating to a score impact that overstates the burden. The coordination layer ensures that a product with one severe concern receives that concern's full weight, not five approximations of it stacked.

**References:**  
- `methodology.md` (Stage 5 — Concern coordination)  
- `constants.py` (family budget constants)  
- `cap_taxonomy.md` (cap proliferation guard)

---

### NR-014

**Subject:** Fortification Non-Credit  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Vitamin and mineral fortification is not credited as a positive signal in BSIP2 scoring. A product fortified with iron, B vitamins, calcium, or vitamin D does not receive a higher score on the nutrient density or any other dimension as a result of that fortification. The score reflects the unfortified food structure.

This applies to both Type 1 (remediation fortification — adding back nutrients removed by processing) and Type 2 (public health fortification — enriching widely consumed foods to address population deficiencies).

**Rationale:**  
Type 1 remediation fortification (e.g., adding B vitamins to refined flour) is partial compensation for processing damage, not a structural quality improvement. The fiber, food matrix, and phytochemicals destroyed by milling are not restored by vitamin addition. Crediting the fortification would reward the processing that necessitated it.

Type 2 public health fortification (e.g., vitamin D in milk, iodine in salt) is a population-level intervention embedded in a product, not a product quality signal. Crediting it would conflate public health policy with food structural quality.

The non-credit treatment creates a known UI transparency requirement: products that are fortified appear equivalent on score to unfortified versions of the same structure. The recommended resolution is a UI note, not an architecture change.

**References:**  
- `beneficial_processing.md` (Fortification section)  
- `edge_case_catalog.md` (Category 3 — Fortified breakfast cereal)

---

### NR-015

**Subject:** Fermentation Direct Bonus  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
Products with confirmed genuine fermentation (identified via ingredient markers: live cultures, lactic acid bacteria, cultured, traditionally fermented) receive a direct scoring bonus of +8 points applied pre-cap, for NOVA 1–3 products only. NOVA 4 products are excluded from the fermentation bonus.

**Rationale:**  
Fermentation is an established form of beneficial processing. It reduces anti-nutrients (phytates), pre-digests protein, produces B vitamins, reduces lactose, and in live-culture products may have probiotic effects. These properties are analytically meaningful and represent genuine structural nutritional improvements. The bonus is pre-cap to ensure it affects the base score before guardrails are applied.

The NOVA 4 exclusion prevents the bonus from relieving the ultra-processing cap for products that use fermentation as a minor component within an otherwise heavily engineered formulation.

**References:**  
- `constants.py` (`FERMENTATION_DIRECT_BONUS = 8`, `NOVA_HP_WEIGHTS`)  
- `beneficial_processing.md` (Fermentation section)  
- `bread-editorial-content.ts` (fermentation zone scoring)

---

### NR-016

**Subject:** Category-Relative Evaluation  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
All BSIP2 dimension scores are evaluated relative to the product's assigned category. Calorie density, protein thresholds, and sugar thresholds are not universal — each category has its own lookup tables and scoring curves. A score of 65 in the `whole_food_fat` calorie density table reflects a different nutritional judgment than a score of 65 in the `beverage` table.

Scores are comparable across products within the same category. Cross-category comparisons are analytically valid only with explicit contextual framing.

**Rationale:**  
A nut butter at 600 kcal/100g and a sports drink at 60 kcal/100ml are not comparable on a single calorie scale. A walnut is not calorie-dense in the same sense as an engineered confection at the same calorie count. Category awareness prevents the system from producing analytically correct but contextually meaningless results.

**References:**  
- `category_analysis.md` (full calorie density tables per category)  
- `methodology.md` (§What makes this different)  
- `constants.py` (`CALORIE_DENSITY_TABLES`)

---

### NR-017

**Subject:** Processing Principle  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
BSIP2's processing concern targets specific industrial practices — high-temperature extrusion that destroys grain structure, fractional extraction that creates isolated macronutrient components, and extensive additive systems that reconstruct palatability — not processing as such. Fermentation, pasteurization, freezing, and cooking are not the targets of processing concern and are not penalized by the processing quality dimension.

The NOVA proxy and additive markers are instruments for identifying the target processes, not for identifying processing generically.

**Rationale:**  
Without this principle, the system would incorrectly penalize beneficial processing (sourdough fermentation, pasteurization for safety, concentration of whole foods) alongside harmful processing (extrusion, fractionation, hyper-palatability engineering). The principle prevents "less processed = better" absolutism and maintains analytical validity.

The principle is documented to prevent architectural drift: future signal additions and cap changes must be tested against it.

**References:**  
- `beneficial_processing.md` (processing evaluation principle)  
- `methodology.md` (Hyper-Palatability detection)

---

### NR-018

**Subject:** Grade Thresholds (v2 Recalibration)  
**Date established:** v2 recalibration — pre-2026-05-30  
**Status:** Active — supersedes v1 thresholds

**Decision:**  
Current operative grade thresholds (v2, as implemented in `constants.py`):

| Grade | Score range |
|-------|-------------|
| S | ≥ 90 |
| A | ≥ 80 |
| B | ≥ 65 |
| C | ≥ 50 |
| D | ≥ 35 |
| E | < 35 |

> Note: The public-facing methodology document (`methodology.md`) describes A: 85–100, B: 70–84, C: 55–69, D: 40–54, E: 0–39. These are the v1 consumer-facing thresholds. The implementation (`constants.py`) uses the v2 recalibrated thresholds above. Alignment of consumer-facing copy with v2 thresholds is a pending documentation task.

**Rationale:**  
The v2 recalibration adjusted thresholds to smooth the grade distribution and prevent grade compression at the top of the scale, where v1 thresholds were producing too few A-grade products for products that were analytically strong. The S grade (≥ 90) was introduced as a ceiling tier to differentiate exceptional whole foods from merely strong products.

**References:**  
- `constants.py` (`GRADE_THRESHOLDS`, `score_to_grade()`)  
- `batch_run_milk_004.py` (v2 recalibration notes)  
- `scoring.md` (known weight/threshold discrepancy note)

---

### NR-019

**Subject:** Snack Bar NOVA 4 Ceiling  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
A snack bar product classified as NOVA 4 faces both the snack bar health-halo cap (NR-002, cap at 70) and the NOVA 4 cap (NR-003, cap at 68). The most restrictive cap wins. In practice, a snack bar at NOVA 4 is capped at 68 before the 70 health-halo cap, making the effective ceiling 68 — grade B upper boundary in v2 thresholds, but frequently lower when sugar, additive, or calorie caps also apply.

The editorial finding is: "NOVA4 is a score ceiling, not a category of bad. When a product is NOVA4, the maximum score it can receive is D" — this reflects the practical outcome after all concurrent caps fire, not the theoretical 68 cap in isolation.

**Rationale:**  
This ruling exists to clarify the interaction between NR-002 and NR-003 for the single most common stress case in the snack category. The distinction matters for consumer communication: the D ceiling for NOVA 4 snack bars is an observed outcome of concurrent caps, not a single rule. Documenting it separately prevents mis-attribution of the ceiling to a single cause.

**References:**  
- `constants.py` (NOVA and calorie cap interaction)  
- `snack-editorial-content.ts` (NOVA4 ceiling framing)  
- `cap_taxonomy.md` (BRC-01, HTC-01)

---

### NR-020

**Subject:** No Imputation Policy  
**Date established:** Pre-2026-05-30  
**Status:** Active

**Decision:**  
BSIP2 does not impute missing nutritional fields. If a field is absent from the product data, it is recorded as absent and the absence reduces analytical confidence. Missing fields do not receive median-category substitutions, historical averages, or regulatory minimums as fill-in values.

Confidence reductions from missing fields:
- Missing fiber: −5
- Missing sodium: −5
- Missing ingredient list: −25
- Low NOVA classification confidence (typically from missing ingredients): up to −10

A product with critical data absent (confidence < 40) is capped at a final score of 50.

**Rationale:**  
Imputation produces false precision. A score produced with imputed values implies analytical confidence that the data does not support. The no-imputation policy forces confidence scores to accurately reflect the analytical quality of the underlying data — which then gates grade display through the confidence ceiling mechanism. A product with a missing ingredient list cannot receive grade A or B; the data quality is insufficient to support those grades.

**References:**  
- `methodology.md` (Stage 1 — Feature extraction)  
- `constants.py` (`CONFIDENCE_INSUFFICIENT_CEILING`, `CONFIDENCE_LOW_CEILING`)  
- `edge_case_catalog.md` (Category 8 — incomplete data)

---

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Active** | Currently operative; implemented in BSIP2 proto v0 |
| **Active (v2 recalibrated)** | Active; specific threshold values were updated in the v2 recalibration run |
| **Superseded** | Previously operative; replaced by a newer ruling (reference is provided) |
| **Under Review** | Operative but flagged for re-examination; may be revised |

---

## Known Tensions (Not Rulings — Documented for Awareness)

These are not rulings. They are documented architectural tensions acknowledged in the framework.

1. **Grade threshold alignment:** The consumer-facing methodology doc (`methodology.md`) uses v1 thresholds; `constants.py` uses v2 thresholds. Alignment is pending.

2. **Serving-size evaluation:** BSIP2 evaluates per 100g. Condiments (miso, soy sauce) and powders (protein powder) present analytically correct but contextually misleading results at this frame. No resolution has been implemented.

3. **Cap gaming surfaces:** Multiple caps have hard numerical thresholds that are single-point gaming surfaces (e.g., 430 kcal, 25g sugar). Gradient transitions are documented as future direction in `cap_taxonomy.md`.

4. **NOVA proxy confidence:** The NOVA classification is an inference, not an observed fact. Cap BRC-01 applies a hard limit on a probabilistic inference. Confidence-weighted penalty is documented as the intended future direction.

5. **Fermentation scoring gap:** The engine cannot distinguish genuine sourdough from industrial sourdough-powder in all cases. The bakery semantics layer addresses this partially; classification errors remain possible.

---

*Registry version: 1.0 | Algorithm version: BSIP2 proto v0 / 0.3.1 | Status: Active*
