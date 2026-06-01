# Known Failure Modes

**Purpose:** Document architectural risks and confirmed scoring traps in BSIP2. Each entry identifies a failure mode, explains why it matters, describes the current mitigation, and characterises the remaining risk. This document is a living record — not a list of fixed problems, but a catalogue of places where the system can go wrong.

The goal is adversarial honesty: a scoring system that cannot name its own failure modes is not a reliable one.

---

## FM-01 — Low-calorie engineered products scoring too high

**Description:**
A product may contain artificial sweeteners, multiple emulsifiers, texture agents, and synthetic flavourings — yet if it carries low sugar, low fat, and low calories, several penalty rules may not fire. The system as currently specified could return a deceptively high score for what is effectively a chemistry experiment with a food label.

**Why it matters:**
The BSIP2 value proposition is food structure interpretation, not calorie auditing. A diet pudding at 60 kcal/100g with six additives and two sweeteners is not a good-quality food — but it may outperform a whole-food product with higher calorie density. This is the single most dangerous category of mis-scoring.

**Current mitigation:**
- `SWEETENER_PRESENT` applies a hard cap at 70 regardless of calorie profile
- Additive markers (3+, 5+) apply their own caps
- NOVA proxy classification should flag such products as NOVA 4, applying the processing cap
- Additive quality dimension scores independently of calorie density

**Remaining risk:**
Moderate. Mitigation depends on NOVA proxy accuracy. If the ingredient-based NOVA inference misses a product (e.g. a novel additive not in the marker list), the product may escape the processing cap and score misleadingly. The sweetener cap is a blunt instrument — it catches sweetener presence but not the full engineered-texture burden.

---

## FM-02 — Whole-food products punished by calorie density rules

**Description:**
Calorie density scoring and guardrail rules use absolute kcal thresholds. A high-fat whole food — dates, coconut products, avocado-based spreads, sesame-based products — can trigger interaction rules designed for engineered snack bars.

**Why it matters:**
Applying snack-bar calorie logic to tahini produces a distorted result. Tahini at 600 kcal/100g is not nutritionally comparable to a 600 kcal/100g cereal bar with glucose syrup and palm oil. The physical matrix, satiation mechanism, and nutritional contribution are fundamentally different.

**Current mitigation:**
- Category-relative calorie density tables (the `whole_food_fat` category uses substantially higher calorie tolerances)
- Whole-food floors: NOVA 1 single-ingredient → minimum score 75; whole-food fat NOVA 1–2 → minimum 65
- The `HIGH_CAL_HIGH_SUGAR_*` rules require both high calories AND high sugar, which typically would not apply to pure nut or seed products

**Remaining risk:**
Low for clearly whole-food products in the `whole_food_fat` category. Moderate for mixed products (e.g. a date-nut bar that is genuinely whole-food but classified as `snack_bar_granola`). Category misclassification converts this from a low risk to a high risk — see FM-08.

---

## FM-03 — Double-counting concerns

**Description:**
The concern coordination system is designed to prevent this, but the architecture contains seams where the same underlying quality failure could be measured twice: once through a guardrail cap, once through a dimension score, and once through an HP pattern.

**Why it matters:**
A product with high fat and high sugar already receives penalties through: the glycemic quality dimension, the fat quality dimension, the `HIGH_CAL_HIGH_SUGAR_*` guardrail rules, and potentially the `HP_FAT_SUGAR_COMBO` hyper-palatability penalty. The concern coordinator handles the guardrail layer, but dimension scoring is entirely independent of guardrail coordination. A product could legitimately receive both dimension-level penalties AND guardrail penalties for the same structural property.

**Current mitigation:**
- Concern coordination covers all guardrail rules (caps and penalties)
- Dimension scoring is separately capped at 100 per dimension and weighted by its assigned fraction; no dimension can exceed its weight contribution
- The separation of layers is intentional: dimensions assess relative nutritional quality; guardrails enforce structural hard stops

**Remaining risk:**
Low for deliberate double-counting between guardrails. Moderate for the interaction between dimension scores and guardrail penalties: a product with severe sugar issues may see its glycemic quality dimension score of 15 already priced in — and then face a sugar-load cap of 45 and an additional −7 penalty. Whether the total impact correctly represents the product's actual quality or overcounts is a calibration question the current specification cannot fully answer.

---

## FM-04 — Cliff-threshold behaviour

**Description:**
Many rules use hard numeric thresholds. A product at 499 kcal/100g and 24.9g sugar/100g receives no `HIGH_CAL_HIGH_SUGAR_SEVERE` cap (threshold: 500 kcal AND 25g sugar). A product at 500 kcal and 25g sugar is capped at 50. The boundary is a cliff, not a slope.

**Why it matters:**
A score difference of 20–30 points between products that are nutritionally near-identical is analytically indefensible. It also makes the score gameable: a manufacturer who reformulates to bring a product from 500 kcal to 498 kcal has made no meaningful nutritional change but escaped a hard cap.

**Current mitigation:**
- Most severe rules have softer counterpart rules at lower thresholds (e.g. `HIGH_CAL_HIGH_SUGAR_MODERATE` at 470/20g fires before the severe cap threshold)
- Dimension scoring is continuous within each dimension, providing gradual signals below guardrail thresholds
- Multiple rules at staggered thresholds create a step-function rather than a pure cliff

**Remaining risk:**
High. The staggered structure reduces the sharpness of individual cliffs but does not eliminate them. Any product near a rule threshold is vulnerable to a large score swing from a small reformulation. The deeper issue is architectural: caps by design are binary (fire / not fire). Making caps continuous would require restructuring the guardrail layer into something closer to continuous penalty scaling, which is a different design philosophy.

---

## FM-05 — Sweetener over-punishment and under-punishment

**Description:**
The current model applies a uniform `SWEETENER_PRESENT` cap (score ≤ 70) regardless of which sweetener, at what quantity, in what food matrix, and for what purpose. A product using stevia in a genuinely low-sugar formulation is treated identically to a product using acesulfame potassium plus sucralose plus aspartame in an ultra-processed dessert.

Additionally, the cap fires only on presence — a trace of sweetener in an otherwise excellent product caps it at the same ceiling as a product whose entire sweetness profile is synthetic.

**Why it matters:**
The 70 cap is deliberately conservative, but it is blunt. It prevents the score from rewarding sweetener substitution as if it were nutritional improvement (correct). But it may also penalize genuine product types where regulated sweetener use is structurally different (e.g. specific medical nutrition products, sports formulations with specific regulatory approval).

**Current mitigation:**
- The cap is explicitly not subject to concern coordination — it fires independently and universally
- The design documentation is explicit: sweetener substitution is not equivalent to quality improvement
- The cap at 70 prevents A or high-B grades, which is intentional

**Remaining risk:**
Moderate. The bluntness is a known limitation, not an oversight. The risk is that product categories with structural sweetener use (sports nutrition, medical nutrition, certain beverage formats) are uniformly pushed below grade B regardless of other signals. This may become a calibration issue when those categories are evaluated at scale.

---

## FM-06 — Protein isolate ambiguity

**Description:**
The `protein_isolate` marker applies a dimension penalty to the protein quality dimension. The logic is that protein from isolated fractions is structurally different from protein in a whole-food matrix. However, not all protein isolates are equivalent: whey protein isolate from bovine milk is structurally and nutritionally different from soy protein isolate in a heavily processed meat alternative. Both currently receive the same marker treatment.

**Why it matters:**
A whey protein isolate-based product used by an athlete as a recovery tool is not meaningfully comparable to a protein-fortified ultra-processed snack. The current system treats the isolate marker as a binary quality signal without accounting for the broader nutritional purpose or food context.

**Current mitigation:**
- The penalty applies at the dimension level only — it reduces protein quality dimension score but does not trigger a guardrail cap
- The nutrient density dimension scores total protein quantity independently, providing a positive signal
- The net effect is a tradeoff representation, not a veto

**Remaining risk:**
Low-moderate. The current approach produces a defensible analytical result (high protein quantity, reduced quality score, net tradeoff) even if it cannot distinguish between isolate use contexts. The risk is that sports/medical products receive ambiguous scores that could be interpreted either direction.

---

## FM-07 — Beneficial processing not recognised

**Description:**
BSIP2 penalizes processing but does not credit beneficial processing. Pasteurisation, fermentation, and certain heat treatments improve safety, bioavailability, and shelf life without adding harmful additives. A fermented dairy product (kefir, yogurt) is processed — but the processing is generally beneficial. The NOVA framework treats all NOVA 3 products uniformly.

**Why it matters:**
Fermented foods, certain cooked legumes, and pasteurised products are processed in ways that improve rather than degrade their nutritional quality. A NOVA 3 cap applied to kefir penalises a product for something that is arguably a nutritional positive.

**Current mitigation:**
- NOVA 3 applies a cap at 75 — this is a relatively mild cap, allowing B and A grades at NOVA 3
- The dairy_protein category has its own calorie threshold table calibrated to the product type
- Fermented dairy products with clean ingredient lists, high protein, and no additives will score well in other dimensions and may largely absorb the NOVA 3 cap in the final result

**Remaining risk:**
Low-moderate. The current design is a known simplification. NOVA 3 as a concern is directionally correct for most processed foods; the failure mode is overreach into genuinely beneficial processing. Explicit fermentation credit is not currently in the architecture.

---

## FM-08 — Category misclassification

**Description:**
Category classification is inferred through name matching, ingredient signals, and retailer classification fields. It is not a database lookup. A product that is ambiguously named, sold in multiple contexts, or categorised inconsistently by retailers can end up in the wrong category — and the wrong category means the wrong calorie threshold table, potentially the wrong cap rules, and wrong comparison context.

**Why it matters:**
A date-nut energy ball classified as `snack_bar_granola` faces the strictest calorie density thresholds and a health-halo cap. The same product classified as `whole_food_fat` would be evaluated much more generously. The category determines much of the analytical context. Misclassification produces results that are internally consistent but externally wrong.

**Current mitigation:**
- Low category confidence (< 0.5) reduces overall analytical confidence by up to −15, triggering a confidence ceiling
- The `default` category applies moderate thresholds — less aggressive than `snack_bar_granola` but not as generous as `whole_food_fat`
- Whole-food floors (NOVA 1 minimum 75) partially protect genuinely whole-food products even when miscategorised

**Remaining risk:**
High in edge cases. The whole-food floor only covers NOVA 1 products. A whole-food product at NOVA 2 that is miscategorised into `snack_bar_granola` has no floor protection and faces the strictest calorie rules. This is the most operationally dangerous failure mode because it can produce radically wrong results for a specific class of products.

---

## FM-09 — Additive ideology leakage

**Description:**
The additive marker system treats the presence of emulsifiers, stabilizers, and synthetic flavourings as a processing signal. This is consistent with the NOVA framework. However, the current marker list may overweight certain additive types or fail to distinguish between additives with very different safety and quality profiles.

**Why it matters:**
Lecithin (a natural emulsifier from sunflowers or eggs) and polysorbate 80 (a synthetic surfactant) both may appear in the same additive category. Treating them equivalently penalizes products for ingredient choices that have different scientific and regulatory standing. This risks the score reflecting ideological positions about "natural vs. artificial" rather than evidence-based quality differences.

**Current mitigation:**
- The additive marker system is based on structural processing signals rather than individual ingredient judgements
- NOVA classification is the primary processing signal; additive markers are a secondary burden indicator
- The marker list is not currently public-facing; it is an analytical intermediate

**Remaining risk:**
Moderate. The risk escalates as the marker list grows. Each new marker added to the list embeds a value judgement about that ingredient. Without explicit criteria for what qualifies as an additive marker and what doesn't, the list becomes an ideological accumulation rather than an analytical instrument.

---

## FM-10 — Health-halo overcorrection

**Description:**
The `snack_bar_granola` category is treated with particular strictness because of its documented health-halo marketing problem. But overcorrection is a symmetric failure: applying overly harsh rules to this category could produce absurd results for genuinely high-quality bars (e.g. a minimal-ingredient, high-protein, whole-food date-nut bar scored worse than a cheaper but slightly lower-calorie product with more additives).

**Why it matters:**
If the harshest category rules systematically disadvantage the best products in that category, the score loses discriminatory power where it matters most. The health-halo concern is real — but a correction so strong that it penalizes the best actors in the category fails the mission.

**Current mitigation:**
- Caps in `snack_bar_granola` fire on specific thresholds (470 kcal + 15g sugar; 430 kcal alone); they do not apply uniformly
- A bar at 350 kcal with high protein, minimal additives, and no red labels can still score well under current rules
- The whole-food floor provides partial protection for NOVA 1 bars

**Remaining risk:**
Moderate. The current threshold structure is calibrated for problematic products in the category. Whether the rules correctly discriminate between health-halo products and genuinely good whole-food bars depends on threshold calibration that is still experimental.

---

## FM-11 — Confidence ceilings hiding good products

**Description:**
A product with genuinely excellent nutritional architecture but an incomplete data record (missing fiber, absent ingredient list from one retailer) may face a confidence ceiling that prevents it from scoring above 70. The ceiling is applied at the score level — not at the dimension level — so there is no mechanism for the user to distinguish "this product scored 65 because it's mediocre" from "this product scored 65 because its data is incomplete."

**Why it matters:**
A whole almond product without a full ingredient list (because it is a single ingredient) may be penalized in confidence for exactly the property that makes it excellent (simplicity). The confidence system cannot currently distinguish "ingredient list absent because product is a single ingredient" from "ingredient list absent because retailer didn't scrape it."

**Current mitigation:**
- The UI language guide specifies that confidence level must be surfaced when below medium
- Low-confidence results should lead with the data gap, not the score
- BSIP1 trust level feeds into analytical confidence, partially tracking data quality provenance

**Remaining risk:**
Moderate. The UI mitigation depends on implementation fidelity. A product that correctly scores 85 but is capped at 70 due to missing data will appear to users as a B-grade product with no visible explanation unless the confidence display is correctly implemented.

---

## FM-12 — Hyper-palatability pattern overreach

**Description:**
The four HP patterns (fat-sugar, fat-sodium, refined carb + fat, crunch-sweet) are calibrated for engineered products designed to exploit reward mechanisms. But the same compositional patterns appear in genuinely whole-food products. Full-fat cheese is high in fat and sodium. A wholesome granola may be high in sugar from dates and high in fat from oats and nuts.

**Why it matters:**
If the HP engine fires on whole-food products because they happen to match the compositional pattern, the system is attributing intentional engineering to natural composition. This is both analytically wrong and potentially misleading to users.

**Current mitigation:**
- HP patterns require both concentration and context — the thresholds are set to reduce false positives on typical whole-food profiles
- NOVA classification provides an upstream signal: an HP pattern on a NOVA 1 product is less analytically significant than on a NOVA 4 product
- Concern coordination limits the total HP penalty through the `hyper_palatability` family budget

**Remaining risk:**
Moderate. The thresholds are currently unverified at scale. Specific product types (full-fat cheese, certain nut clusters, whole-food energy products) may trigger HP patterns that their composition doesn't actually represent as an engineered quality.

---

## FM-13 — Ultra-processed but nutritionally decent products

**Description:**
Some NOVA 4 products have genuinely good nutritional profiles: high protein, moderate calories, minimal sugar, adequate fiber. A protein shake with significant NOVA 4 characteristics (multiple additives, protein isolate, sweeteners) may deliver a nutritional architecture that a simpler but less complete product does not match.

**Why it matters:**
BSIP2 cannot purely be a processing proxy. If a NOVA 4 product genuinely delivers more useful nutrition than a NOVA 2 product, the score should reflect the tradeoff — not simply rank processing above nutrition. The analytical mission is food structure interpretation, not NOVA replication.

**Current mitigation:**
- Dimension scoring is independent; processing quality, nutrient density, and protein quality are separate dimensions
- A NOVA 4 processing cap limits the maximum score but doesn't prevent the nutrient density dimension from reflecting protein and fiber content
- The score produces a tradeoff representation rather than a veto

**Remaining risk:**
Moderate. The concern is that the cumulative effect of NOVA cap + additive cap + sweetener cap + HP penalty leaves a nutritionally reasonable product at a score that does not reflect its actual contribution relative to less nutritious but cleaner alternatives. Calibration data is needed.

---

## FM-14 — Culturally biased assumptions

**Description:**
The analytical framework embeds implicit assumptions about food quality that reflect Northern European and American nutritional science conventions. Products culturally central to Middle Eastern, South Asian, or East Asian diets may be misevaluated: tahini is high-fat; miso is high-sodium; pickled vegetables carry sodium without the same health concern as processed sodium.

**Why it matters:**
If BSIP2 systematically disadvantages foods that are central to non-Western dietary patterns and central to well-established dietary traditions, the score is not a neutral analytical instrument. It is encoding a cultural preference dressed as nutritional science.

**Current mitigation:**
- Tahini and nut products are explicitly handled by the `whole_food_fat` category and calorie tolerance structure
- Sodium thresholds are set at levels that affect genuinely high-sodium engineered products (≥ 700mg/100g) rather than moderate traditional uses
- The whole-food floor protects NOVA 1 and NOVA 2 products regardless of calorie or fat profile

**Remaining risk:**
Moderate. The framework handles the most obvious cases but has not been systematically audited against the full range of traditional food products that appear in the Israeli market context (the initial target). High-sodium traditional foods (olives, pickles, certain cheeses, preserved fish) may score poorly for structural reasons that don't reflect their actual dietary role.
