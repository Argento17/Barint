# Bari Distortion Backlog v1

**Type:** Research backlog — structured inventory only  
**Authority:** Research Analyst  
**Sources read:** Evidence Registry v1 (BEV-062 to BEV-066), `classification_instability.md`, `structural_emptiness_concept.md`, `cap_taxonomy.md`, `evaluation_scope.md`, `positive_architecture_framework.md`, `ingredient_fragmentation_concept.md`  
**Date:** 2026-05-30  

This document does not propose fixes. It inventories every known systematic distortion in BSIP2 scoring, assesses what is known about each, and orders them for research prioritisation. A distortion is a systematic deviation between what the score implies and what the analytical reality is — not a calibration error, not a future feature, but a structural gap that produces misleading results today.

---

## Distortion Inventory

---

### DIST-001 — Dairy Fiber Penalty

**Also recorded as:** DISTORTION-001 in `governance_v1.md`; BEV-062 in Evidence Registry

**Description:**  
The nutrient density dimension uses the formula: `0.65 × protein_score + 0.35 × fiber_score`. This formula applies a 35% weight to fiber regardless of product category. Dairy products are biologically fiber-free. The formula penalises dairy for the absence of a nutrient that dairy does not and cannot contain — not for any formulation weakness. The penalty is applied to every dairy product in the system, every time it is scored, with no category adjustment.

**Impacted categories:** `dairy_protein` (yogurts, quark, skyr, cottage cheese, kefir); any future dairy category.

**Evidence strength:** Strong. The distortion is quantified with a specific formula and measured per product. Scale of distortion confirmed at 0.84–4.46 final score points depending on protein level. Example documented: יופלה GO (10g protein, 72 kcal) scores 70/B; without the fiber penalty would score 72/B. The distortion increases as protein content increases — the most nutritionally dense dairy products are most affected.

**Estimated scoring impact:** 0.84–4.46 points of systematic underscoring per product. Direction: always negative (dairy is always underscored relative to its analytical reality). At the grade boundary (B/C threshold at 70), a 2-point distortion is grade-determinative.

**Difficulty to resolve:** Low-medium. The fix is a formula change in `score_engine.py`: exempt dairy products from the fiber weight in the nutrient density calculation. Requires: (1) cross-category regression to confirm no unintended effects on non-dairy categories, (2) boundary audit to identify any products whose grade changes at the B/C or A/B threshold, (3) governance review because grade changes affect published scores.

---

### DIST-002 — Date Sugar Halo

**Also recorded as:** BEV-063 in Evidence Registry

**Description:**  
Date bars and date-dominant products contain 60–70% total sugars by weight. Under the current architecture, these sugars are treated structurally differently from added refined sugar: dates are NOVA 1–2, the ingredient list is short, and the sugar comes from a whole-food source. The result is that a date bar scoring well on structural simplicity can carry glycemic impact equal to products that receive explicit cap penalties for their sugar content. The architecture's position — natural sugar ≠ added refined sugar at equivalent concentration — is a defensible analytical philosophy. The distortion is not the scoring outcome but the silence around it: the position is embedded in scoring rules without being surfaced to consumers or documented in methodology copy.

**Impacted categories:** `snack_bar_granola` primarily; potentially `sauce_spread` (date-based spreads, fig jam), `dessert` (date-sweetened confectionery).

**Evidence strength:** Moderate-strong. The phenomenon is well-described and confirmed by the CE Advisory verdict on snack bars. The analytical position (natural vs. added sugar structural distinction) is documented and accepted. The evidence gap is quantitative: the actual glycemic impact comparison between date-sugar products and penalised-sugar products has not been empirically measured against the Bari corpus.

**Estimated scoring impact:** Unknown magnitude. Direction: positive (date-dominant products score higher than products with equivalent total sugar from refined sources). The score gap between a date bar and a sugar-syrup bar at equivalent total sugar concentrations is not documented.

**Difficulty to resolve:** Medium. The scoring philosophy itself is not necessarily wrong. The distortion is primarily one of transparency — the position is not disclosed. Resolution requires: (1) a quantified comparison between date-sugar and added-sugar product scores at equivalent concentrations, (2) a decision on whether the philosophical position should be retained, modified, or explicitly disclosed, (3) implementation of disclosure in methodology copy and product-level confidence notes if retained.

---

### DIST-003 — Router v2 Missing Archetypes (Bread / Cracker)

**Also recorded as:** BEV-064 in Evidence Registry

**Description:**  
Router v2 does not have dedicated archetypes for `bread` and `cracker` product classes. The bread-light stress test (32 synthetic products) identified three confirmed failure modes: (1) seed-topped bread routes as `whole_food_fat` (WFF contamination — the seed signal overrides the bread signal); (2) cracker products have no routing target and fall to `default`; (3) beverages and dairy-protein products have documented false-positive risk. Products routed to the wrong category are scored against incorrect calorie density tables and category-specific caps — the scoring is internally consistent but analytically invalid.

**Impacted categories:** `bread` (production impact), `cracker` (production impact), `whole_food_fat` (contamination from misrouted bread), `default` (contamination from misrouted crackers). Future categories involving seed-rich or grain-dominant products are at risk.

**Evidence strength:** Strong. The failure modes are documented from the bread-light stress test. The seed-topped bread WFF contamination case is the most thoroughly documented: the mechanism is understood (seed anchor overrides bread classification signal), the consequence is understood (applies WFF rules to a bread product), and the score impact is calculable.

**Estimated scoring impact:** High in individual cases. A seed-topped whole grain sourdough bread routed to `whole_food_fat` instead of `bread` will face WFF category calorie density scoring — which is more lenient than bread scoring. Quantified impact not measured against production corpus; the bread-light corpus was synthetic. At volume, a significant fraction of seed-toppped breads may be mislabelled.

**Difficulty to resolve:** Medium. Requires new router archetypes for bread and cracker product classes. The signals needed (grain-dominant ingredient list, typical bread calorie range, Hebrew category keywords) are known. The implementation requires: (1) defining anchor conditions for `bread` and `cracker`, (2) adding bread/cracker archetypes to router_v2.py, (3) cross-category regression to confirm no new conflicts, (4) running bread-light validation corpus against updated router.

---

### DIST-004 — Prototype Weight Divergence

**Also recorded as:** BEV-065 in Evidence Registry

**Description:**  
The 10 dimension weights in `constants.py` are prototype values established during initial engine development. They sum to 1.0 but were not derived from calibration against a validated corpus. The public-facing methodology document uses different weights. Any analytical conclusion that treats current `constants.py` weights as the intended or final weights is drawing on uncalibrated parameters. The system is currently producing scores with weights that may not reflect the design intent.

**Impacted categories:** All categories. All 10 dimensions are affected. Products near grade boundaries are most at risk of grade misassignment due to uncalibrated weights.

**Evidence strength:** Moderate. The divergence between `constants.py` and the methodology document is confirmed. The direction and magnitude of scoring error introduced by uncalibrated weights is unknown because no calibration corpus exists against which to measure. This is the weakest-evidence distortion in the list — we know the weights are wrong but we do not know how wrong or in which direction.

**Estimated scoring impact:** Unknown. Potentially 5–15 final score points for products where the most-deviant-weighted dimensions are active. Direction: unknown. Products that score primarily on dimensions where current weights over- or under-weight relative to intent will be systematically biased, but the direction is uncharacterised.

**Difficulty to resolve:** High. Requires a corpus-level calibration study: (1) define a golden set of products with known intended grades, (2) run the engine with current weights and measure deviation, (3) iterate weight adjustments until calibration targets are met, (4) document the calibrated weights as final, (5) update the methodology document to match. This is a research-intensive task, not a code change.

---

### DIST-005 — Inactive Scoring Layers (Snacks)

**Also recorded as:** BEV-066 in Evidence Registry

**Description:**  
The four-layer scoring architecture requires nutritional data (protein, sugar, fat, fiber, calories) to activate Layers 2 (Nutritional Contribution) and 3 (Metabolic Stability). The snacks dataset has null nutrition values for all 18 products in the current corpus — BSIP0 captured the packaging images but the nutritional content was not ingested into the BSIP1 enrichment pipeline. As a result, snack bar scores reflect only Layers 1 (Structural Integrity) and 4 (Consumption Engineering). Additionally, 11 products in the snacks corpus are labelled `confidence: verified` despite having no verified nutritional content. The confidence label is factually incorrect.

**Impacted categories:** `snack_bar_granola` (snacks corpus, 18 products). This is a data availability distortion specific to the current snacks corpus, not an architectural distortion.

**Evidence strength:** Strong. The null nutrition values in the snacks JSON are a measurable fact. The confidence label mismatch is documented in the CE Advisory verdict. The score mean convergence (snacks 43.50 ≈ maadanim 43.78) is noted as "not analytically credible" — date bars and chocolate puddings should not have equivalent mean scores.

**Estimated scoring impact:** Potentially 10–20 points per product when nutritional data is ingested and Layers 2–3 activate. Direction: mixed — some products currently scoring above their nutritional reality (those whose structural signals are stronger than their nutritional profile) will score lower; some products currently under-penalised for poor nutritional contribution will score lower. Products with strong nutritional profiles may score higher.

**Difficulty to resolve:** Low-medium (data ingestion is the immediate step; score recalibration follows). Requires: (1) nutritional data extraction from BSIP0 captures for all 18 snack products, (2) BSIP1 re-enrichment with nutritional fields populated, (3) BSIP2 re-score of snacks corpus, (4) confidence label correction for all 11 incorrectly labelled products, (5) frontend JSON regeneration.

---

### DIST-006 — Classification Instability

**Documented in:** `01_framework/bsip2_framework/docs/classification_instability.md` (not in Evidence Registry distortion section)

**Description:**  
BSIP2 applies fundamentally different analytical frameworks depending on product category assignment. The same product scored in two different categories can produce a score difference of 20–40 points — not because the product changed, but because the evaluation frame changed. This is by design: category-relative scoring is correct. The distortion arises from the fragility of the classification itself: category assignment is an L3 inference with imperfect confidence, but the scoring engine applies category rules at full severity regardless of classification confidence. A confident-but-wrong classification produces an internally consistent score that is analytically invalid, with no signal in the output that anything is wrong.

**Confirmed scenario:** A date-almond-oat ball at 480 kcal/100g (NOVA 2) correctly assigned to `whole_food_fat` scores ~70–80 (grade B). Misassigned to `snack_bar_granola`, the same product scores ~45–55 (grade D). The 30-point gap is produced entirely by the wrong category frame. The score of ~50 looks plausible; there is nothing in the output to indicate the frame is wrong.

**Four failure modes documented:** (1) Ambiguous form factor — energy balls, oat bars, granola toppings that fit multiple categories; (2) Cross-language classification — products named entirely in Hebrew without category keywords fall through; (3) Novel product categories — functional beverages, high-protein dairy innovations, plant-based dairy have no good category match; (4) NOVA misclassification — NOVA proxy inference can be confidently wrong for a product whose NOVA-triggering ingredients are not in the detectable ingredient marker set.

**Impacted categories:** All categories. Highest risk at category boundaries: products that could plausibly be `snack_bar_granola` or `whole_food_fat`; `beverage` or `dairy_protein`; `cereal` or `snack_bar_granola`. Explicitly documented as "the single biggest practical scoring risk in BSIP2."

**Evidence strength:** Strong. The mechanism is fully characterised, the example is fully worked (score ~70–80 vs. ~45–55 for the same product), four failure mode types are catalogued. The empirical prevalence in the production corpus is not measured — we do not know what fraction of live products are miscategorised.

**Estimated scoring impact:** 20–40 points in confirmed worst-case scenarios. Direction: typically negative for whole-food products that fall into `snack_bar_granola` (most penalising category). For products that fall into `default` instead of their correct category, impact direction depends on the correct category: `snack_bar_granola` defectors improve; `dairy_protein` or `whole_food_fat` defectors worsen.

**Difficulty to resolve:** High. Full resolution requires architectural changes: (1) tracking and surfacing `category_confidence` as a first-class output field (currently an internal diagnostic); (2) implementing severity-scaled category rules (blended score when confidence is 0.50–0.79; default rules when confidence < 0.50); (3) secondary-category simulation to surface high-sensitivity products before scoring; (4) defining explicit archetypes for high-risk ambiguous product forms (date-nut bars, avocado spreads, oat-based snacks). Partial mitigation (flagging low-confidence classifications) is achievable in one sprint.

---

### DIST-007 — Structural Emptiness Blind Spot

**Documented in:** `01_framework/bsip2_framework/docs/structural_emptiness_concept.md` (not in Evidence Registry distortion section)

**Description:**  
A product can achieve a moderate BSIP2 score not by delivering nutritional value but by engineering around penalty triggers. Low calorie density means calorie rules do not fire. No added sugar means glycemic quality is not penalised. No detectable additives. No red labels. Nothing fires. The score emerges as 62–68 — passable, maybe B-minus territory. But the product delivers near-zero protein, near-zero fiber, and no food matrix of nutritional consequence. It is architecturally engineered to be inoffensive to the scoring system rather than nutritionally present.

The calorie density dimension actively contributes to this distortion: it rewards lower calorie density, so a product at 40 kcal/100g of flavoured water and modified starch receives a high calorie density score for being nutritionally absent. This is a dimension inversion — the dimension designed to penalise caloric excess inadvertently rewards nutritional vacancy.

**Canonical examples documented:** Diet mousse (40 kcal, near-zero protein/fiber, heavy sweetener and stabiliser system); zero-sugar gelatin dessert (8 kcal, flavoured water + gelatin protein that is nutritionally incomplete); heavily flavoured rice cakes (350 kcal, 2.5g protein, 0.8g fiber, but moderate score because nothing fires).

**Impacted categories:** `dessert`, `beverage`, and any category where low-calorie-density products are evaluated. Particularly affects diet product variants that replace caloric content with bulking agents and sweeteners.

**Evidence strength:** Moderate-strong. Multiple canonical examples are documented with the specific gaps identified. The calorie density dimension inversion is clearly characterised. The empirical prevalence in the production corpus — how many live products score passably due to structural emptiness rather than nutritional quality — is not measured.

**Estimated scoring impact:** 5–15 points of positive distortion for structurally empty products relative to their nutritional reality. The distortion is difficult to quantify without a positive architecture comparison point — we can only establish the upper bound by asking "what would a product that delivered genuine nutritional value at this calorie density score?"

**Difficulty to resolve:** High. Resolution requires the positive architecture framework — a set of signals that detect and credit nutritional presence, not just penalise nutritional absence. The calorie density dimension inversion can be partially addressed by a matrix poverty flag (very low calorie + very low protein + very low fiber + very low fat = no calorie density credit) without requiring the full positive architecture. But complete resolution requires implementing at least partial positive signals.

---

### DIST-008 — Cliff-Edge Cap Gaming Surfaces

**Documented in:** `01_framework/bsip2_framework/docs/cap_taxonomy.md` (partial overlap with BEV-053 in Evidence Registry)

**Description:**  
Four hard caps in BSIP2 have single-threshold cliff edges where the difference between a score cap triggering and not triggering is 0.1g of a nutrient or 1 kcal. A product reformulated from 25.2g to 24.8g sugar has made no meaningful nutritional change but escapes the HIGH_SUGAR_25G_PLUS cap. The scoring jump at the threshold is 0 to a 60-point ceiling — a binary outcome from a continuous input. This is not a scoring error for any individual product at any given time; it is a structural invitation to reformulate products to the near-threshold rather than genuinely improving them.

**The four high-risk caps:**
- `HIGH_SUGAR_25G_PLUS`: cliff at 25g sugar/100g; high gaming risk
- `HIGH_SODIUM_700MG_PLUS`: cliff at 700mg sodium/100g; high gaming risk; also problematic for condiments used in small quantities
- `ADDITIVE_MARKERS_3_PLUS`: cliff at 3 additive markers; moderate gaming risk (removing one additive is real reformulation)
- `NOVA_PROXY_4`: hard cap when NOVA 4 is inferred; moderate gaming risk (borderline NOVA 3/4 products)

**Impacted categories:** All categories for the sugar and sodium caps. `snack_bar_granola` for the snack-specific heuristic caps (HTC-01, HTC-02, HTC-03 add three more gaming surfaces). `sauce_spread` is disproportionately affected by the sodium cap (miso, soy sauce, preserved condiments).

**Evidence strength:** Strong for the structural characterisation (the cap_taxonomy.md analysis is thorough). Empirical evidence of gaming — actual reformulation to threshold — is not available in the Bari corpus. The gaming risk is prospective, not observed.

**Estimated scoring impact:** The distortion is not a current scoring error but a structural vulnerability. At individual product level: any product that sits within 5% of a cap threshold is within reformulation range to escape. The scoring impact of cap escape is the cap value itself: escaping the 25g sugar cap changes the score from ≤60 to uncapped — a potential upward shift of 10–20 points for high-scoring products.

**Difficulty to resolve:** Medium-high. Resolution requires gradient cap design — replacing binary thresholds with continuous penalty curves. The cap_taxonomy.md documents the gradient approach. Implementation requires: (1) defining the gradient function for each of the four caps (start point, end point, steepness), (2) cross-category regression to confirm gradient scores correlate correctly with cap scores, (3) calibration against the golden products suite.

---

### DIST-009 — Condiment Per-100g Evaluation

**Documented in:** `01_framework/bsip2_framework/docs/evaluation_scope.md` (not in Evidence Registry)

**Description:**  
BSIP2 evaluates all products per 100g. For foods consumed in 100g quantities, this is the correct analytical frame. For condiments consumed in small quantities (5–15g per use) — miso, soy sauce, fish sauce, hot sauce, preserved olives, capers — the per-100g frame produces scores that imply a level of sodium intake orders of magnitude larger than actual consumption. Miso paste at 3,000–6,000mg sodium/100g triggers every sodium guardrail at full force. The score is analytically correct per-100g but practically misleading: a consumer who uses a teaspoon of miso in soup is not consuming the same sodium burden implied by the score.

**Impacted categories:** `sauce_spread` primarily. Edge cases in `beverage` (concentrated flavour drops), `snack_bar_granola` (flavour powders). The distortion is category-contained but within `sauce_spread` it may affect a significant fraction of products.

**Evidence strength:** Moderate. The mechanism is well-understood and clearly characterised. The empirical extent of the distortion in the `sauce_spread` corpus is not measured — how many sauce_spread products are condiments vs. spread-quantity foods is unknown.

**Estimated scoring impact:** Significant for affected products. Miso paste at 4,000mg sodium/100g would score near zero on the sodium dimension and trigger multiple caps. A realistic per-serving sodium load from miso (one tablespoon = ~15g) delivers ~600mg sodium — below the Israeli red label threshold. The per-100g score and the per-serving nutritional reality are not in the same order of magnitude.

**Difficulty to resolve:** Medium. Two partial mitigations are feasible without architecture changes: (1) surface a context note in the UI for `sauce_spread` products identified as small-quantity condiments: "This product is typically used in small quantities. Score reflects per-100g composition."; (2) add a `context_limited` flag to the output for identified condiment product types. Full resolution requires serving-size-adjusted evaluation, which is a significant data infrastructure change.

---

### DIST-010 — Incomplete Protein Credit

**Documented in:** `01_framework/bsip2_framework/docs/structural_emptiness_concept.md` (not in Evidence Registry)

**Description:**  
BSIP2 credits protein by quantity (g/100g) without distinguishing nutritional completeness. Gelatin protein (~8g/100g in gelatin desserts) is credited identically to complete protein from whole-food sources. Gelatin is a hydrolysed collagen protein that lacks the essential amino acid tryptophan — it is nutritionally incomplete and cannot substitute for dietary complete protein. A gelatin-based dessert product showing 8g protein on the label receives the same protein quality signal as a product with 8g complete protein. The system reads the label; it cannot read behind the label.

A secondary form of this distortion applies to highly fragmented protein isolates: whey protein isolate, pea protein isolate, and soy protein concentrate are all credited equivalently to protein in intact food sources, despite differing degrees of ingredient fragmentation and differing digestibility profiles.

**Impacted categories:** `dessert` (gelatin-based products), `dairy_protein` (protein isolate products), `snack_bar_granola` (protein bars with isolate). Low product count in production corpus.

**Evidence strength:** Moderate. The gelatin case is well-documented in the structural emptiness concept with the specific biochemical reason (tryptophan absence). The isolate vs. whole-food protein question is characterised conceptually but not quantified in the Bari corpus. Empirical prevalence is not measured.

**Estimated scoring impact:** Low-moderate for individual products. The distortion would produce overscoring for gelatin-protein products (possibly 3–7 points on the protein quality dimension) and ambiguous credit for isolate-protein products. In practice, gelatin-rich products typically have many other signals that limit their score; the protein credit may not be the determinative factor.

**Difficulty to resolve:** High. Distinguishing complete from incomplete protein requires: (1) a protein completeness detection system in BSIP1 (identifying gelatin, collagen, partial-protein sources in ingredient lists), (2) a confidence-weighted protein quality signal that discounts non-complete protein, (3) validation against a corpus that includes gelatin-protein products. This requires new Hebrew ingredient taxonomy entries and a new signal extraction rule.

---

## Prioritized Research Backlog

Prioritisation criteria: (1) Breadth — how many categories and products are affected; (2) Magnitude — how many points of scoring distortion; (3) Evidence quality — how well-characterised is the distortion; (4) Systemic risk — does the distortion produce misleading results that consumers or operators cannot detect.

---

### Tier 1 — Research Priority: High

These distortions affect the most products, produce the largest scoring deviations, or represent systematic risks that are active in production today.

| Rank | ID | Distortion | Why Tier 1 |
|---|---|---|---|
| 1 | DIST-006 | Classification instability | 20–40pt swings; all categories; invisible in output; self-described as "single biggest practical scoring risk" |
| 2 | DIST-007 | Structural emptiness blind spot | Systematic architecture gap; calorie dimension inverted for empty products; affects philosophy of what a good score means |
| 3 | DIST-001 | Dairy fiber penalty | Quantified (up to 4.46pts); systematic; affects every dairy product in production; grade-determinative at boundaries |
| 4 | DIST-005 | Inactive scoring layers (snacks) | Confidence labels factually wrong today; all 18 snack products underscored on nutritional dimensions; immediately actionable |

---

### Tier 2 — Research Priority: Medium

Real distortions with real scoring consequences, but either narrower in scope, less immediately actionable, or partially mitigated by existing mechanisms.

| Rank | ID | Distortion | Why Tier 2 |
|---|---|---|---|
| 5 | DIST-003 | Router v2 missing archetypes | Up to 30pt swings for affected products; known failure modes; gets worse as bread corpus grows |
| 6 | DIST-002 | Date sugar halo | Defensible philosophy; primary issue is disclosure absence, not scoring error per se |
| 7 | DIST-008 | Cliff-edge cap gaming surfaces | Prospective risk, not observed; but structural invitation is real; four caps affected |
| 8 | DIST-004 | Prototype weight divergence | Affects all categories; magnitude unknown; cannot be assessed without calibration corpus |

---

### Tier 3 — Research Priority: Low

Documented, real, but narrow in scope, low empirical prevalence in current corpus, or dependent on earlier-tier work.

| Rank | ID | Distortion | Why Tier 3 |
|---|---|---|---|
| 9 | DIST-009 | Condiment per-100g evaluation | Category-contained; partial mitigation available without architecture change; product count in corpus is low |
| 10 | DIST-010 | Incomplete protein credit | Low product count; likely not grade-determinative for most affected products; dependent on DIST-007 infrastructure |

---

## Relationship to Evidence Registry

| Distortion ID | Evidence Registry entry | Status in registry |
|---|---|---|
| DIST-001 | BEV-062 | Under Review |
| DIST-002 | BEV-063 | Under Review |
| DIST-003 | BEV-064 | Under Review |
| DIST-004 | BEV-065 | Under Review |
| DIST-005 | BEV-066 | Under Review |
| DIST-006 | Not registered | Documented in framework docs only |
| DIST-007 | Not registered | Documented in framework docs only |
| DIST-008 | BEV-053 (partial) | Under Review (caps accepted; gradient is Future Work) |
| DIST-009 | Not registered | Documented in evaluation_scope.md only |
| DIST-010 | Not registered | Documented in structural_emptiness_concept.md only |

**Note:** DIST-006, DIST-007, DIST-009, and DIST-010 are not registered in the Evidence Registry. They should be added as new BEV entries to close the gap between framework documentation and the institutional memory record.

---

## Distortion Summary Table

| ID | Distortion | Categories | Evidence | Impact (pts) | Difficulty | Priority |
|---|---|---|---|---|---|---|
| DIST-001 | Dairy fiber penalty | dairy_protein | Strong | 0.84–4.46 (systematic) | Low-Med | Tier 1 |
| DIST-002 | Date sugar halo | snack_bar_granola | Mod-Strong | Unknown, positive bias | Medium | Tier 2 |
| DIST-003 | Router v2 missing archetypes | bread, cracker, WFF | Strong | Up to 30 (case-specific) | Medium | Tier 2 |
| DIST-004 | Prototype weight divergence | All | Moderate | 5–15 (unknown direction) | High | Tier 2 |
| DIST-005 | Inactive scoring layers | snack_bar_granola | Strong | 10–20 (mixed direction) | Low-Med | Tier 1 |
| DIST-006 | Classification instability | All | Strong | 20–40 (negative for WFF) | High | Tier 1 |
| DIST-007 | Structural emptiness blind spot | dessert, beverage | Mod-Strong | 5–15 (positive bias) | High | Tier 1 |
| DIST-008 | Cliff-edge cap gaming | All (4 caps) | Strong | 10–20 (when escaped) | Med-High | Tier 2 |
| DIST-009 | Condiment per-100g evaluation | sauce_spread | Moderate | Significant (local) | Medium | Tier 3 |
| DIST-010 | Incomplete protein credit | dessert, dairy, snacks | Moderate | 3–7 (overscoring) | High | Tier 3 |

---

*End of Distortion Backlog v1. Next distortion entry: DIST-011.*
