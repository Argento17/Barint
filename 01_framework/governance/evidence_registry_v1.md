# Bari Evidence Registry v1

**Type:** Institutional memory document  
**Scope:** All evidence, rulings, and accepted positions incorporated into Bari as of 2026-05-30  
**Authority:** Research Analyst  
**Status:** Active — append-only; never delete or overwrite entries  

---

## How to Read This Registry

Each entry records a piece of knowledge that has been accepted, rejected, or placed under review within the Bari system. Entries are not ranked by importance. New entries are added at the bottom of their section; IDs are permanent.

**Impact codes:**
- **Scoring** — affects how BSIP2 calculates or caps scores
- **Interpretation** — affects how signals are named or framed in consumer output
- **Dataset** — affects how products are categorised, enriched, or validated
- **Content** — affects editorial language, copy standards, or methodology disclosure
- **Future Work** — accepted as correct but not yet implemented; queued for BSIP3 or V2

---

## Optional `study_objects:` block (added TASK-196, 2026-06-06)

Any entry in this registry MAY include an optional `study_objects:` YAML block containing one or more structured per-study records. This is **backward-compatible**: entries without a `study_objects:` block are valid and complete. No migration of existing entries is required.

**Schema:** `01_framework/governance/evidence_study_schema.py` — Python dataclass with 7 fields.  
**How to fill it in:** `01_framework/governance/evidence_grading_sop_v1.md` — plain-language grading guide.

Format (placed as a fenced YAML block directly below the entry table):

```yaml
study_objects:
  - claim: "One sentence describing what the study claims"
    dose_realistic: true          # true if study dose ≤ 2× real label dose
    population_direct: true       # true if population matches Israeli general-consumer
    rob_grade: "low"              # low | moderate | high | very_high
    evidence_tier: "A"            # A=Strong | B=Moderate | C=Weak | D=Insufficient
    source_doi: "10.XXXX/..."     # DOI, "PMID:XXXXXXX", or "internal:[doc-name]"
    notes: "Caveats, conflicts of interest, effect sizes, population limits"
```

**Governance rules:**
- Study objects are authored by the Research Agent.
- Nutrition Agent co-signs the tier assignment for any entry already marked `should_affect_score_now: true`.
- A `study_objects:` block does NOT, by itself, create a scoring rule or move any published score.
- Applies equally to the BSIP2 EV-### registry and the SUPP-EV-### supplement registry.

---

## Section 1 — Core Framework & Philosophy

### BEV-001
**Topic:** Bari's analytical boundary  
**Summary:** Bari evaluates structural food composition, not individual health outcomes. It produces population-level structural interpretation, not individual dietary prediction or recommendation. The governing Hebrew formulation is "ברי מתאר. לא ממליצה" (Bari describes. Does not recommend.)  
**Source:** `01_framework/governance/governance_v1.md`; `01_framework/bsip2_framework/framework_philosophy.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-002
**Topic:** Three credible claim types  
**Summary:** Bari can credibly make exactly three types of claim: (1) Structural description — documentable label facts, always defensible; (2) Structural interpretation — probabilistic population-level conclusions bounded by evidence; (3) Normative judgment — explicit value-based assessments per design commitments. Claims of individual health prediction are outside scope.  
**Source:** `01_framework/bsip2_framework/framework_philosophy.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-003
**Topic:** What Bari explicitly is not  
**Summary:** Bari is not: (a) a nutrient-threshold scoring system; (b) a pure NOVA scoring system; (c) an anti-processing ideology; (d) a low-calorie optimisation system; (e) a dietary recommendation engine; (f) a health certification body; (g) a product quality ranker on an absolute scale; (h) a replacement for professional advice.  
**Source:** `01_framework/bsip2_framework/framework_philosophy.md`; `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-004
**Topic:** Six signal layers epistemological model  
**Summary:** All signals are classified in six layers — L1 (observed facts from label), L2 (derived ratios and deterministic calculations), L3 (inferred classifications with confidence scoring), L4 (threshold-based interpreted concerns), L5 (population-level behavioral hypotheses), L6 (normative design commitments). This taxonomy governs how each signal is justified and how much certainty it carries.  
**Source:** `01_framework/bsip2_framework/signal_taxonomy.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-005
**Topic:** Three-layer consumer communication model  
**Summary:** Consumer output is constrained to three layers: Layer 1 (observable label fact), Layer 2 (analytical conclusion bounded by Layer 1), Layer 3 (plain-language translation that cannot exceed Layer 2). The rule of layer containment — Layer 3 ≤ Layer 2 ≤ Layer 1 — is a hard editorial constraint, not a style preference.  
**Source:** `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-006
**Topic:** Framework invisibility principle  
**Summary:** Internal systems — FQC, GSS, archetypes, BSIP pipeline stages, dimension names, signal codes — never surface in consumer copy. The sophistication of the internal analysis is inversely proportional to how technical the output should sound. A reader with zero framework knowledge should fully understand Bari's consumer output.  
**Source:** `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-007
**Topic:** Intent attribution prohibition  
**Summary:** Bari never attributes intent to manufacturers. Documentation records what is present in the label, not why it is there. "Contains glucose syrup" is valid. "Uses glucose syrup to increase palatability" is not a Bari claim.  
**Source:** `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-008
**Topic:** Structural-first over nutrient-threshold  
**Summary:** Bari's governing question is not "Does this product meet nutrient RDIs?" but "Is the composition consistent with what the product presents itself as? What is the food matrix integrity?" A single-ingredient whole food scores well regardless of macro profile (e.g., olive oil at 900 kcal/100g). A low-calorie engineered product with sweetener and stabilisers scores poorly despite meeting a calorie threshold.  
**Source:** `01_framework/bsip2_framework/framework_philosophy.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-009
**Topic:** Transparency over simplification  
**Summary:** When signals conflict, surface the conflict. When data is partial, label it partial. When uncertainty exists, disclose it. The worst handling of uncertainty is a score displayed as though underlying data were complete. Complexity in data is preferred over simplified hiding.  
**Source:** `01_framework/bsip2_framework/framework_philosophy.md`; `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation, Dataset  

---

### BEV-010
**Topic:** Anti-drift governance: ten questions  
**Summary:** Before publishing any consumer-facing output, ten questions must be checked: (1) Does this sound like a recommendation? (2) Are we describing or judging? (3) Are we implying intent we cannot verify? (4) Is this emotionally loaded? (5) Would this survive legal review? (6) Does this sound like a wellness app? (7) Are we over-explaining the framework? (8) Is uncertainty visible enough? (9) Is the article driven by evidence or narrative desire? (10) Could a reasonable manufacturer dispute this wording?  
**Source:** `01_framework/governance/governance_v1.md`  
**Status:** Accepted  
**Impact:** Content  

---

## Section 2 — Scoring Architecture

### BEV-011
**Topic:** BSIP2 six-stage pipeline  
**Summary:** BSIP2 scores products through six sequential stages: (1) feature extraction (~50 analytical features from nutrition panel and ingredient list), (2) dimension scoring (10 dimensions, 0–100 each, weighted), (3) guardrail evaluation (veto rules, hard caps, soft penalties, floors), (4) hyper-palatability detection (4 patterns), (5) concern coordination (prevents double-counting), (6) final resolution (apply caps, penalties, floors, confidence ceiling, clamp to 0–100).  
**Source:** `01_framework/bsip2_framework/methodology.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-012
**Topic:** Ten scoring dimensions and prototype weights  
**Summary:** The 10 dimensions and their current prototype weights: Processing Quality 18%, Nutrient Density 16%, Calorie Density Quality 12%, Glycemic Quality 11%, Protein Quality 9%, Additive Quality 7%, Satiety Support 6%, Fat Quality 6%, Regulatory Quality 4%, Whole Food Integrity 1%. These are prototype values in `constants.py`; they are not identical to the public-facing methodology weights. Calibration is deferred.  
**Source:** `01_framework/bsip2_framework/methodology.md`; `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted (weights are prototype — calibration is Future Work)  
**Impact:** Scoring  

---

### BEV-013
**Topic:** Grade scale A–E  
**Summary:** A = 85–100 (strong across most dimensions, no significant structural concerns); B = 70–84 (good overall, minor concerns); C = 55–69 (meaningful concerns, acceptable in context); D = 40–54 (multiple concerns, not recommended as regular choice); E = 0–39 (significant structural issues, hard caps or veto applied).  
**Source:** `01_framework/bsip2_framework/methodology.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-014
**Topic:** Concern coordination — double-counting prevention  
**Summary:** When multiple scoring rules address the same root concern (e.g., high sugar), the primary signal is kept at full weight and secondary signals in the same concern family are demoted. Five concern families with budget limits: SUGAR_FAMILY, SODIUM_FAMILY, CALORIE_FAMILY, PROCESSING_FAMILY, FAT_QUALITY_FAMILY. This prevents a single product weakness from generating disproportionate total penalty.  
**Source:** `01_framework/bsip2_framework/methodology.md`; `03_operations/bsip2/proto_v0/src/score_engine.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-015
**Topic:** Category-relative scoring principle  
**Summary:** All dimension scores are evaluated against category-specific thresholds, not universal benchmarks. 350 kcal/100g in `whole_food_fat` category ≠ 350 kcal/100g in `snack_bar_granola`. Cross-category comparison is analytically problematic and requires user-facing transparency about what category each product belongs to.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-016
**Topic:** Eight product categories with distinct thresholds  
**Summary:** The eight scoring categories are: `whole_food_fat`, `snack_bar_granola`, `dessert`, `beverage`, `dairy_protein`, `cereal`, `sauce_spread`, `default`. Each has category-specific calorie density tables that define how calorie density maps to dimension scores. See BEV-041 to BEV-048 for individual category calibrations.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring, Dataset  

---

### BEV-017
**Topic:** Router v2 — three-stage product routing  
**Summary:** Router v2 replaces v1 category classifier. Three stages: (1) anchor stage — hard product-class anchors (nuts, seeds, plain yogurt); (2) context-gated signals — WFF contamination prevention, beverage gate, dairy-protein suppression; (3) resolution — final category from signal composite. Validated against a 12-case golden corpus and 163-product analysis.  
**Source:** `03_operations/bsip2/proto_v0/src/router_v2.py`; `03_operations/bsip2/proto_v0/src/generate_router_validation.py`  
**Status:** Accepted (with known gaps — see BEV-067)  
**Impact:** Scoring, Dataset  

---

### BEV-018
**Topic:** Confidence ceiling mechanism  
**Summary:** Low-confidence products cannot score above their ceiling regardless of structural signals. Ceilings: Insufficient (<40 confidence) → score capped at 50; Low (40–59) → capped at 70; Medium (60–79) → no ceiling; High (80–100) → no ceiling. This prevents false precision from partial data.  
**Source:** `01_framework/bsip2_framework/confidence_framework.md`; `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-019
**Topic:** Confidence score construction — penalty amounts  
**Summary:** Confidence starts at 100 and is reduced by: missing energy/protein/carbs/fat (−10 each), missing fiber/sodium (−5 each), missing ingredient list entirely (−25), suspicious data patterns e.g. sugar > total carbs (−20), low NOVA confidence (up to −10 scaled), low category confidence (up to −15 scaled).  
**Source:** `01_framework/bsip2_framework/confidence_framework.md`  
**Status:** Accepted  
**Impact:** Scoring, Dataset  

---

### BEV-020
**Topic:** Minimum sibling gap principle  
**Summary:** Products with fewer than 2 structural differences should have a score gap of at least 5 points. When two structurally similar products score within 1–2 points, it creates false precision that implies analytical distinctions that do not exist in the data. This rule prevents meaningless micro-rankings.  
**Source:** CE Advisory; `02_products/snack_bars/reports/verdict_v1.md`  
**Status:** Under Review (identified as required; not yet implemented in engine)  
**Impact:** Scoring  

---

## Section 3 — Processing Science Positions

### BEV-021
**Topic:** NOVA classification system — accepted as primary processing signal  
**Summary:** BSIP2 uses NOVA as the primary processing-level signal. NOVA 1 = unprocessed/minimally processed (floor 75); NOVA 2 = processed culinary ingredients; NOVA 3 = processed food (hard cap 75); NOVA 4 = ultra-processed (hard cap 60). NOVA is used as a proxy inferred from ingredient list, not directly reported by manufacturers.  
**Source:** `01_framework/bsip2_framework/methodology.md`; `03_operations/bsip2/proto_v0/src/nova_proxy.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-022
**Topic:** Processing penalties in Processing Quality dimension  
**Summary:** Specific ingredient penalties applied to Processing Quality dimension: NOVA 4 (−24), NOVA 3 (−12), glucose syrup (−8), maltodextrin (−8), flavourings (−6), emulsifiers (−6). Each ingredient beyond 8 in the list incurs −1.2 to the dimension. Additive burden: 3–4 markers caps score at 65; 5+ caps at 55.  
**Source:** `03_operations/bsip2/proto_v0/src/score_engine.py`; `03_operations/bsip2/proto_v0/src/signal_extractor.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-023
**Topic:** Fermentation is structurally beneficial processing  
**Summary:** Fermentation produces documented structural benefits: protein pre-digestion, anti-nutrient reduction, lactose reduction, B vitamin production, and preservation. These are population-level biological facts, not individual claims. Current BSIP2 handling: fermented dairy and grains correctly routed to NOVA 1–2. Fermentation is not yet explicitly credited as a positive signal.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Accepted (current handling correct; explicit positive credit deferred to Future Work)  
**Impact:** Scoring, Future Work  

---

### BEV-024
**Topic:** Pasteurisation has negligible nutritional impact  
**Summary:** Pasteurisation eliminates pathogens with minimal nutrient loss at pasteurisation temperatures. Bari's current handling — no signals generated for pasteurisation — is correct. No change needed.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-025
**Topic:** Freezing preserves nutritional content without additives  
**Summary:** Freezing is a preservation method that requires no additives and maintains nutritional content, often superior to fresh produce in transit. Bari's current handling — no signals generated — is correct.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-026
**Topic:** Concentration versus fragmentation distinction  
**Summary:** Concentration (water removal) is a different process from fragmentation (extracting one component from its matrix). Fruit juice concentrate = refined sugar equivalent (fragmentation logic applies). Concentrated whole-food products retain more structural coherence. Current calorie density tables partially account for this; explicit documentation of the distinction is deferred.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Under Review  
**Impact:** Scoring, Future Work  

---

### BEV-027
**Topic:** Cooking increases bioavailability — no signal required  
**Summary:** Cooking improves protein digestibility, increases bioavailability of specific nutrients (lycopene in tomatoes), and deactivates anti-nutritional factors in legumes. Bari's current handling — no specific signals generated — is appropriate because cooking is an expected processing step, not a differentiating signal between products in the same category.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-028
**Topic:** Fortification: structural credit rejected; transparency required  
**Summary:** BSIP2 does not credit fortification in the scoring architecture. Rationale: fortification does not change structural food integrity. Two fortification types exist — remediation (nutrients added back post-processing damage) and public health (enriching widely consumed food). Neither changes the structural assessment. Risk: fortified and unfortified products appear equivalent; UI transparency is required but not architecture change.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`  
**Status:** Accepted (no scoring credit); UI transparency noted as Future Work  
**Impact:** Scoring, Content, Future Work  

---

### BEV-029
**Topic:** Hyper-palatability: four accepted patterns  
**Summary:** Four hyper-palatability patterns are incorporated into BSIP2: (1) Fat-Sugar — fat ≥20% of calories AND sugar ≥20% of calories; (2) Fat-Sodium — fat ≥25% of calories AND sodium ≥300mg/100g; (3) Refined Carb + Fat — carbs ≥40% AND fat ≥15% AND fiber/carb ratio ≤10%; (4) Crunch-Sweet — carbs ≥50g AND sugar ≥20g AND fiber ≤5g AND fat ≤10g. These are population-level structural hypotheses (L5 signals), not individual behavioural claims.  
**Source:** `01_framework/bsip2_framework/docs/processing_analysis.md`; `03_operations/bsip2/proto_v0/src/score_engine.py`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-030
**Topic:** Hyper-palatability amplifiers and moderators  
**Summary:** Amplifiers increase the hyper-palatability penalty: chocolate coating (+15%), glucose syrup or maltodextrin (+15%), extruded grain (+15%), flavourings (+5%), emulsifiers (+5%). Moderators reduce it: intact nuts or seeds (−15%), whole grains (−8%), dates or fruit paste (−8%). Two triggered patterns apply a hard cap of 60; three or more apply a hard cap of 50.  
**Source:** `03_operations/bsip2/proto_v0/src/score_engine.py`; `01_framework/bsip2_framework/docs/processing_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-031
**Topic:** Hyper-palatability term does not appear in consumer copy  
**Summary:** "Hyper-palatability" is an analytically precise clinical term but should not appear in consumer-facing language. Consumer framing uses pattern-specific descriptions: "This product combines high fat and high sugar — a pattern associated with engineered taste reward"; "High fat and sodium concentration"; "Low-fiber refined grain and fat combination"; "High sugar, low fiber cereal structure."  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

## Section 4 — Nutritional Science Positions

### BEV-032
**Topic:** Whole-food matrix superiority over isolate  
**Summary:** Protein from isolate (whey isolate, pea isolate) is nutritionally functional but structurally different from protein in its original food matrix. 15g protein from intact Greek yogurt ≠ 15g protein from whey isolate in a manufactured bar. Bari credits protein quantity but distinguishes protein source in interpretation signals.  
**Source:** `01_framework/bsip2_framework/docs/positive_architecture_framework.md`; `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-033
**Topic:** Structural satiety vs. macro satiety  
**Summary:** Food structure contributes to satiety independent of macronutrient content. An apple (50 kcal, intact fiber, chewing required) produces different satiety signal than apple juice (45 kcal, no fiber, no structural resistance). Whole almonds ≠ almond oil at the same caloric equivalence. Current BSIP2 handles this partially through satiety support dimension; explicit structural satiety positive signal is Future Work.  
**Source:** `01_framework/bsip2_framework/docs/positive_architecture_framework.md`  
**Status:** Accepted (partial implementation); full positive signal deferred  
**Impact:** Scoring, Future Work  

---

### BEV-034
**Topic:** Liquid calorie effect — no satiety compensation  
**Summary:** Liquid-form calories do not trigger equivalent satiety response to solid food at the same caloric level. Beverage category receives the strictest calorie density thresholds because liquid calories do not compensate for reduced solid food intake. This is the primary reason plant-based milks score in the C–D range regardless of other signals.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`; `01_framework/bsip2_framework/methodology.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-035
**Topic:** Soy protein is the only plant-milk protein source with functional significance  
**Summary:** Among plant milks, soy is the only variety with a meaningful protein contribution (~3–4g/100ml). Other plant milks (oat, almond, coconut, rice) have protein values too low to function as a meaningful protein source. This finding justified the score premium for soy milk over other plant milks in the milk category.  
**Source:** `02_products/milk_and_alternatives/reports/executive_summary.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-036
**Topic:** Native fiber vs. added/extracted fiber  
**Summary:** Structural fiber — fiber native to the food matrix (oat beta-glucan in intact oats, pectin in intact apple) — differs from supplemental extracted fiber (chicory inulin, oat fiber extract). Both are legitimate, but structural origin carries different signal weight. Matrix-native fiber contributes to both nutritional and structural scores; added fiber contributes primarily to nutritional credit at reduced weight. Full positive signal implementation is Future Work.  
**Source:** `01_framework/bsip2_framework/docs/positive_architecture_framework.md`  
**Status:** Under Review (partial; full implementation is Future Work)  
**Impact:** Scoring, Future Work  

---

### BEV-037
**Topic:** Glycemic quality: sugar + fiber interaction  
**Summary:** Glycemic quality scoring accounts for the relationship between sugar content and fiber content. High sugar content partially offset by high fiber content produces a different metabolic plausibility signal than high sugar with low fiber. The fiber/carb ratio is a calculated L2 signal used in both glycemic quality dimension and hyper-palatability pattern detection.  
**Source:** `01_framework/bsip2_framework/methodology.md`; `03_operations/bsip2/proto_v0/src/score_engine.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-038
**Topic:** Israeli Ministry of Health red label thresholds — accepted as external reference  
**Summary:** The Israeli Ministry of Health red label thresholds are incorporated as external regulatory signals: Sugar ≥17.5g/100g, Saturated fat ≥5.0g/100g, Sodium ≥600mg/100g. These are L1 observable facts that trigger regulatory concern signals. Bari does not endorse these thresholds as nutritionally optimal — they are a regulatory reference point.  
**Source:** `03_operations/bsip2/proto_v0/src/constants.py`; `01_framework/bsip2_framework/methodology.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-039
**Topic:** Fat quality: saturated fat as a secondary signal  
**Summary:** Fat quality dimension penalises high saturated fat proportion and rewards whole-food fat sources. The penalty is applied at the dimension level, not as a cap. Palm oil and coconut oil are treated as saturated fat sources. Nuts and seeds as primary ingredient are credited as whole-food fat sources. Fat quality accounts for 6% of final score.  
**Source:** `01_framework/bsip2_framework/methodology.md`; `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-040
**Topic:** Non-nutritive sweeteners: score cap, not veto  
**Summary:** Presence of any non-nutritive sweetener triggers a hard cap of 70. This is a normative L6 commitment — a design choice, not a direct health claim. It reflects Bari's position that sweeteners indicate engineered palatability management. This is not a claim that sweeteners are harmful; it is a claim that sweetener presence is a relevant structural signal.  
**Source:** `01_framework/bsip2_framework/docs/cap_taxonomy.md`; `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

## Section 5 — Category Calibrations

### BEV-041
**Topic:** whole_food_fat category thresholds  
**Summary:** Category for nuts, seeds, nut butters, tahini. Calorie density table: ≤350 kcal = 90; ≤900 = 55; >900 = 45. Rationale: Pure fat products approach 900 kcal/100g; the range accommodates the natural variation in whole-food fat products. Whole-food floor: minimum final score of 65 for NOVA 1–2 products in this category.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-042
**Topic:** snack_bar_granola category thresholds — strictest in system  
**Summary:** Category for bars, granola, energy bars. Calorie density: ≤150 kcal = 90; ≤430 = 40; >500 = 15. Additional hard caps: ≥430 kcal cap at 70 (HTC-01); red label sugar cap at 55 (HTC-02); ≥470 kcal AND sugar ≥15g cap at 60 (HTC-03). Rationale: Health-halo risk category — products marketed as healthy while carrying caloric and sugar loads comparable to confectionery. Strictest thresholds in the system.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`; `01_framework/bsip2_framework/docs/cap_taxonomy.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-043
**Topic:** beverage category thresholds — second strictest  
**Summary:** Category for drinks, juices, plant milks, protein shakes. Calorie density: ≤10 kcal = 95; ≤70 = 50; >100 = 15. Strict rationale: liquid calories bypass satiety signals and do not compensate for reduced solid food intake (see BEV-034). The near-zero threshold for water-like beverages reflects that caloric beverages compete with a zero-calorie alternative.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-044
**Topic:** dairy_protein category thresholds  
**Summary:** Category for yogurts, quark, skyr, cottage cheese. Calorie density: ≤80 kcal = 90; ≤250 = 55; >350 = 25. The ≤80 kcal upper threshold reflects full-fat plain yogurt (~80–100 kcal/100g) which should earn a strong calorie density score. High protein density is the defining characteristic of this category.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-045
**Topic:** cereal category thresholds  
**Summary:** Category for breakfast cereals, muesli, porridge. Calorie density: ≤300 kcal = 85; ≤430 = 55; >550 = 15. Calibrated so plain oats (~380 kcal/100g) score in the good range within this category. Minimally processed whole grain cereals are intended to score well.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-046
**Topic:** dessert category thresholds  
**Summary:** Category for biscuits, cakes, confectionery. Calorie density: ≤150 kcal = 85; ≤350 = 55; >520 = 15. Products evaluated as treat foods, not meal replacements. Lower structural expectations than functional food categories.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-047
**Topic:** sauce_spread category thresholds  
**Summary:** Category for condiments, dips, hummus, jams. Calorie density: ≤150 kcal = 90; ≤600 = 50; >750 = 25. Wide range captures structural difference between light hummus (~150 kcal) and chocolate spread (~600 kcal) within the same category.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-048
**Topic:** default category thresholds  
**Summary:** Fallback for unclassified products. Calorie density: ≤150 kcal = 90; ≤550 = 35; >550 = 20. Penalising thresholds used for unclassified products to prevent gaming through classification avoidance.  
**Source:** `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

## Section 6 — Hard Cap & Floor Rules

### BEV-049
**Topic:** Trans fat — full veto  
**Summary:** Detection of trans fat above threshold triggers a score floor of 20 — effectively a veto. This is the only full veto in the BSIP2 system. Trans fat has no known safe intake level at population scale. This is an L6 normative commitment.  
**Source:** `03_operations/bsip2/proto_v0/src/constants.py`; `01_framework/bsip2_framework/docs/cap_taxonomy.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-050
**Topic:** NOVA 1 single-ingredient whole-food floor  
**Summary:** Single-ingredient NOVA 1 whole foods receive a minimum final score of 75, regardless of dimension scores. Rationale: the penalty architecture was calibrated for engineered products and would incorrectly penalise natural whole foods (e.g., plain nuts, plain olive oil). This is a NOVA1_SINGLE_FLOOR constant in the engine.  
**Source:** `03_operations/bsip2/proto_v0/src/constants.py`; `01_framework/bsip2_framework/category_analysis.md`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-051
**Topic:** Whole-food fat floor  
**Summary:** Whole-food fat products (NOVA 1–2: nuts, seeds, nut butters, tahini, unrefined oils) receive a minimum final score of 65. Distinct from BEV-050 because this category may have more than one ingredient. Both floors are implemented in `constants.py`.  
**Source:** `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-052
**Topic:** 17 hard caps — complete inventory  
**Summary:** Three safety caps (SC): sweetener present → ≤70; trans fat → veto (=20); 2+ red labels → ≤45. Four structural moderation caps (SMC): sugar ≥25g → ≤60; kcal ≥500 AND sugar ≥25g → ≤50; kcal ≥470 AND sugar ≥20g → ≤60; kcal ≥500 AND protein <6g AND fiber <3g → ≤55; sodium ≥700mg → ≤60; saturated fat red label → ≤55. Four behavioral-risk caps (BRC): NOVA 4 → ≤60; NOVA 3 → ≤75; additive markers 3–4 → ≤65; additive markers 5+ → ≤55. Three heuristic temporary caps (HTC, snack bar only): ≥430 kcal → ≤70; red sugar label → ≤55; ≥470 kcal AND sugar ≥15g → ≤60. Most restrictive cap wins when multiple apply.  
**Source:** `01_framework/bsip2_framework/docs/cap_taxonomy.md`; `03_operations/bsip2/proto_v0/src/constants.py`  
**Status:** Accepted  
**Impact:** Scoring  

---

### BEV-053
**Topic:** Four caps flagged for gradient transition  
**Summary:** Four hard caps are identified as highest gaming risk and as candidates for gradient replacement: HIGH_SUGAR_25G_PLUS (cliff at 25g), HIGH_SODIUM_700MG_PLUS (cliff at 700mg), ADDITIVE_MARKERS_3_PLUS (count-based; gradient more defensible), NOVA_PROXY_4 (confidence-weighted graduation preferred). Gradient design is deferred to BSIP3.  
**Source:** `01_framework/bsip2_framework/docs/cap_taxonomy.md`  
**Status:** Under Review (caps accepted; gradient transition is Future Work)  
**Impact:** Scoring, Future Work  

---

## Section 7 — Product-Level Rulings

### BEV-054
**Topic:** Milk & alternatives category findings — CE Advisory ruling  
**Summary:** Five tier structure confirmed: B-tier (73–75) = whole dairy, full-fat, natural, goat milks; C-tier (56–66) = enriched dairy + plain soy; D-tier (43–51) = plant alternatives (except soy); E-tier (36–40) = engineered protein shakes. No A-grade products exist in this category — structural ceiling imposed by the liquid, dilute nature of all milks. Dominant driver: NOVA classification.  
**Source:** `02_products/milk_and_alternatives/reports/executive_summary.md`  
**Status:** Accepted  
**Impact:** Scoring, Interpretation  

---

### BEV-055
**Topic:** Three consumer misconceptions corrected — milk category  
**Summary:** Three specific consumer misconceptions are documented as analytically incorrect: (1) "Plant milk is healthier than dairy" — false; structural assessment favours full-fat dairy; (2) "Unsweetened = structurally clean" — false; processing level remains regardless of sweetener absence; (3) "More protein = better" — false; protein source and category context matter.  
**Source:** `02_products/milk_and_alternatives/reports/executive_summary.md`  
**Status:** Accepted  
**Impact:** Interpretation, Content  

---

### BEV-056
**Topic:** Snack bars CE Advisory ruling — moderate revision required  
**Summary:** CE Advisory verdict: MODERATE REVISION required (not KEEP, not REBUILD). Philosophy and relative rankings are defensible. Identified problems requiring action: (1) URGENT — nutritional data not ingested despite BSIP0 capture; (2) 11 products labelled "verified" but with no verified nutritional content — confidence labelling incorrect; (3) Score mean convergence (snacks 43.50 ≈ maadanim 43.78) not analytically credible; (4) False precision in D-band (1–2 point gaps between similar products). Date sugar halo requires disclosure (see BEV-063).  
**Source:** `02_products/snack_bars/reports/verdict_v1.md`  
**Status:** Accepted  
**Impact:** Scoring, Dataset, Content  

---

### BEV-057
**Topic:** Snack bars recalibration rules R-01 through R-06  
**Summary:** Six recalibration rules accepted: R-01, R-02, R-03 apply to snacks and bread. R-04 provides dairy sugar relief for milk/yogurt accuracy if needed. R-05 is referenced but not detailed in available documentation. R-06 adds whole grain primary bonus (should-have, not urgent). Implementation pending nutritional data ingestion.  
**Source:** `02_products/snack_bars/reports/verdict_v1.md`  
**Status:** Under Review (accepted in principle; not yet implemented)  
**Impact:** Scoring  

---

### BEV-058
**Topic:** Bread expected grade changes post-recalibration  
**Summary:** Expected grade changes for bread category after R-01 through R-03 application: sourdough whole grain B → A (approximately 3–5 products); standard whole grain stays B but score increases; low-quality standard stays C (59–64); spelt crackers stay A but score rises 2–5 points.  
**Source:** `02_products/snack_bars/reports/verdict_v1.md`; MVP rollout plan  
**Status:** Under Review (projected; not yet validated against live data)  
**Impact:** Scoring  

---

### BEV-059
**Topic:** Four-category MVP rollout status — as of 2026-05-30  
**Summary:** Live status: Milk = LIVE (hand-curated, 18 products); Snacks = LIVE but needs rescore before promotion (18 products, no nutritional data); Bread = LIVE but in wrong component format (24 products, needs component swap + rescore, ~1 day); Yogurts = NOT READY (no data collected, blocked, ~2 days to create).  
**Source:** MVP rollout plan `01_framework/`  
**Status:** Accepted (status accurate as of registry date)  
**Impact:** Dataset  

---

### BEV-060
**Topic:** Bread JSON grade mismatch — known data error  
**Summary:** A known data error exists in the bread frontend JSON: products with score 80 are labelled grade B in the JSON instead of grade A. This is a JSON generation or mapping error, not a scoring engine error. Requires correction before next category promotion.  
**Source:** MVP rollout plan; CE Advisory bread review  
**Status:** Accepted (error documented; correction is pending)  
**Impact:** Dataset  

---

### BEV-061
**Topic:** Yogurt corpus — proposed MVP list  
**Summary:** 12 products proposed for the yogurt MVP corpus: plain whole (תנובה, ביו), flavoured (דנונה, יופלה), high-protein (יופלה GO), dessert (מילקי), non-dairy (סויה, קוקוס), Greek (יוגורט יווני), drinking (לבן גבישים), sweetened (סנו לייף). No data collected as of registry date.  
**Source:** MVP rollout plan  
**Status:** Under Review (list accepted; data collection not started)  
**Impact:** Dataset  

---

## Section 8 — Known Distortions & Open Issues

### BEV-062
**Topic:** DISTORTION-001 — Dairy fiber penalty  
**Summary:** The nutrient density dimension formula (0.65 × protein_score + 0.35 × fiber_score) applies a 35% weight to fiber. Dairy products are biologically fiber-free; this structure penalises dairy for not having fiber, not for any formulation weakness. Scale of distortion: 0.84–4.46 final score points depending on protein level. Example: יופלה GO (10g protein, 72 kcal) currently scores 70/B; under normalised formula would score 72/B. Documented. Not patched. Deferred to BSIP3.  
**Source:** `01_framework/governance/governance_v1.md` (DISTORTION-001)  
**Status:** Under Review (distortion confirmed; fix deferred to BSIP3)  
**Impact:** Scoring, Future Work  

---

### BEV-063
**Topic:** Date sugar halo — unhandled structural gap  
**Summary:** Date bars containing 60–70% total sugars score well on structural simplicity (short ingredient list, NOVA 1–2) but carry glycemic impact equal to products that receive cap penalties. Bari's current position — structural distinction is real; natural sugar ≠ added refined sugar at equal concentration — is defensible as a philosophy choice. However, the position must be disclosed, not silently embedded. Required: explicit disclosure in methodology copy and product-level confidence framing.  
**Source:** `02_products/snack_bars/reports/verdict_v1.md`  
**Status:** Under Review (position accepted; disclosure not yet implemented)  
**Impact:** Scoring, Content, Interpretation  

---

### BEV-064
**Topic:** Router v2 known gaps — bread and cracker archetypes  
**Summary:** Router v2 does not yet have dedicated archetypes for `bread` and `cracker` product classes. Known failure modes: seed-topped bread routes as `whole_food_fat` (WFF contamination); beverage false-positive risk; dairy-protein false-positive risk. Identified in bread-light stress test (32 synthetic products). These are not bugs in live production categories but become active risks when bread and cracker products are processed at volume.  
**Source:** `03_operations/bsip2/proto_v0/src/router_v2.py`; bread-light stress test  
**Status:** Under Review (gaps documented; fixes are Future Work)  
**Impact:** Scoring, Future Work  

---

### BEV-065
**Topic:** BSIP2 weight calibration — prototype values not public  
**Summary:** The 10 dimension weights in `constants.py` are prototype values that sum to 1.0 but differ from the weights documented in the public-facing methodology. Calibration against a full validated corpus has not been completed. Any analysis that treats current weights as final should note this limitation.  
**Source:** `03_operations/bsip2/proto_v0/src/constants.py`; `01_framework/bsip2_framework/methodology.md`  
**Status:** Under Review (prototype weights accepted for current use; calibration is Future Work)  
**Impact:** Scoring, Future Work  

---

### BEV-066
**Topic:** Four-layer architecture activation — two layers inactive for snacks  
**Summary:** The four-layer architecture (Structural Integrity, Nutritional Contribution, Metabolic Stability, Consumption Engineering) is structurally sound. For snack bars, Layers 2 (Nutritional) and 3 (Metabolic) are inactive due to missing nutritional data. Scores computed on snacks reflect only structural/processing signals. This is documented but not surfaced to consumers, which creates a transparency gap.  
**Source:** `02_products/snack_bars/reports/verdict_v1.md`; `01_framework/bsip2_framework/architecture_v2/layer_architecture.md`  
**Status:** Under Review (architecture accepted; activation blocked by data gap)  
**Impact:** Scoring, Content  

---

## Section 9 — Future Architecture Commitments

### BEV-067
**Topic:** V2 four-layer architecture — accepted design direction  
**Summary:** The V2 architecture replaces the single weighted-dimension model with four functionally distinct layers: Layer 1 — Structural Integrity (does this still behave like food?); Layer 2 — Nutritional Contribution (does this materially nourish?); Layer 3 — Metabolic Stability (how physiologically stable is this?); Layer 4 — Consumption Engineering (was this optimised for overconsumption?). Layer 4 is inverted: high score = high concern. Cross-layer tensions surface as visible product profiles, not resolved to a mean.  
**Source:** `01_framework/bsip2_framework/architecture_v2/layer_architecture.md`  
**Status:** Accepted as design direction (not yet implemented)  
**Impact:** Future Work  

---

### BEV-068
**Topic:** Positive architecture — nourishment-present framing  
**Summary:** Current scoring frame: good score = few concerns detected. Accepted future frame: good score = positive structures detected AND few concerns detected. Six positive concept categories to be implemented: Food Matrix Integrity, Structural Satiety, Whole-Food Coherence, Fermentation as Structural Value, Meaningful Protein Density, Meaningful Fiber Density (see individual entries). Addresses the current asymmetry where a low-calorie engineered product with no signal triggers can score comparably to a whole food.  
**Source:** `01_framework/bsip2_framework/docs/positive_architecture_framework.md`  
**Status:** Accepted as design direction (not yet implemented)  
**Impact:** Future Work  

---

### BEV-069
**Topic:** Fermentation explicit credit — Future Work  
**Summary:** Fermentation should eventually reduce processing penalty and contribute a positive structural signal. The change requires: (1) a fermentation detection flag in BSIP1 enrichment, (2) a validated signal extraction rule in `signal_extractor.py`, (3) cross-category regression to confirm no unintended effects. Currently, fermented products benefit implicitly from NOVA 1–2 routing but receive no explicit fermentation credit.  
**Source:** `01_framework/bsip2_framework/docs/beneficial_processing.md`; `01_framework/bsip2_framework/docs/positive_architecture_framework.md`  
**Status:** Accepted as Future Work  
**Impact:** Scoring, Future Work  

---

### BEV-070
**Topic:** Gradient caps — Future Work  
**Summary:** Four current cliff-edge caps (see BEV-053) are accepted as candidates for gradient replacement. Gradient design means: instead of a hard cap at a threshold, a smooth penalty curve that increases proportionally beyond the threshold. This reduces gaming risk at the exact threshold boundary. Design is deferred to BSIP3; current cliff caps remain in production until then.  
**Source:** `01_framework/bsip2_framework/docs/cap_taxonomy.md`  
**Status:** Accepted as Future Work  
**Impact:** Scoring, Future Work  

---

## Section 10 — Language & Editorial Rulings

### BEV-071
**Topic:** Positive signal language — approved formulations  
**Summary:** Approved language for positive signals in consumer output: "High protein — whole food source"; "Good fiber content" or "Fiber-rich"; "Simple ingredient list" (≤8 ingredients); "Minimally processed" (NOVA 1); "No regulatory warnings"; "Contains whole grain"; "Whole food fat source". Absence of a positive signal is not reported (absence of concern is not a feature).  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-072
**Topic:** Negative signal language — approved formulations  
**Summary:** Approved language for negative signals: "Ultra-processed" (NOVA 4); "Processed" (NOVA 3); "Israeli red label: sugar/sodium/saturated fat"; "Multiple regulatory warnings" (2+ red labels); "Contains non-nutritive sweetener"; "High additive complexity" (3–4); "Very high additive complexity" (5+); "Engineered fat-sugar combination"; "High fat-sodium concentration"; "Refined carb and fat combination"; "High sugar, low fiber cereal pattern"; "Contains refined starch derivative"; "Contains trans fat"; "Complex ingredient list" (>12); "Multiple added sugar sources"; "Protein from isolate"; "High calorie density for [category]"; "High calorie, high sugar combination"; "Low satiety signals"; "Ingredient data unavailable."  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-073
**Topic:** Grade language — approved formulations  
**Summary:** Approved grade-level framing: A = "Strong nutritional structure"; B = "Good overall profile"; C = "Some areas of concern"; D = "Notable structural concerns"; E = "Significant analytical concerns." Rejected: "Healthy/Unhealthy" (binary, value-laden); "Clean/Dirty" (not analytical); "Good for you/Bad for you" (personalised advice); "Approved/Not approved" (false certification); "Natural" (undefined, not used in analysis).  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-074
**Topic:** Forbidden terms — complete list  
**Summary:** Terms that must never appear in Bari consumer output: "Superfoods"; "Clean eating"; "Guilt-free"; "Detox"; "Boosts immunity" / "Supports [organ]"; "AI-powered analysis" (inaccurate — engine is deterministic, not ML); "Our algorithm thinks..." (signals should be specific, not attributed to a generic algorithm); "Better for you"; "Nutritionist approved." Also forbidden: "Hyper-palatability" in consumer copy (use pattern-specific description instead — see BEV-031).  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-075
**Topic:** Confidence language — approved framing by band  
**Summary:** High confidence (80–100): display score and grade without qualification. Medium (60–79): display with brief note "Based on available data." Low (40–59): display with caveat "Some nutrition data missing — result is an estimate." Insufficient (<40): do not lead with score; surface data gap with "Not enough information to assess this product reliably." Do not display grade without surfacing confidence level when confidence is medium or lower.  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

### BEV-076
**Topic:** Dimension display labels — approved consumer names  
**Summary:** Dimension internal names map to consumer labels: Processing Quality → "Processing"; Nutrient Density → "Nutrient density"; Calorie Density Quality → "Calorie density"; Glycemic Quality → "Glycemic quality"; Protein Quality → "Protein"; Additive Quality → "Additives"; Satiety Support → "Satiety"; Fat Quality → "Fat quality"; Regulatory Quality → "Regulatory signals"; Whole Food Integrity → "Whole food character". Dimension scores below 40 indicate meaningful concern; above 70 indicate meaningful strength.  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content  

---

### BEV-077
**Topic:** Tradeoff language — no false reassurance  
**Summary:** When a product has genuine tradeoffs, the UI must surface the tension rather than collapse it into a verdict. Example: protein bar with high protein from isolate and a sweetener — correct framing is "High protein content from isolate. Contains non-nutritive sweetener. Hard cap applied." Not "High protein snack with some concerns." Example: high-calorie nut butter — correct framing is "Whole food fat source. High calorie density evaluated against nut product thresholds." Not "Good choice despite high calories." The language explains the analysis; it does not perform reassurance.  
**Source:** `01_framework/bsip2_framework/ui_language.md`  
**Status:** Accepted  
**Impact:** Content, Interpretation  

---

## Registry Summary

| Section | ID Range | Count | Notes |
|---|---|---|---|
| Core Framework & Philosophy | BEV-001 – BEV-010 | 10 | All Accepted |
| Scoring Architecture | BEV-011 – BEV-020 | 10 | BEV-020 Under Review |
| Processing Science Positions | BEV-021 – BEV-031 | 11 | BEV-026 Under Review |
| Nutritional Science Positions | BEV-032 – BEV-040 | 9 | BEV-036 Under Review |
| Category Calibrations | BEV-041 – BEV-048 | 8 | All Accepted |
| Hard Cap & Floor Rules | BEV-049 – BEV-053 | 5 | BEV-053 Under Review |
| Product-Level Rulings | BEV-054 – BEV-061 | 8 | Mixed |
| Known Distortions | BEV-062 – BEV-066 | 5 | All Under Review |
| Future Architecture | BEV-067 – BEV-070 | 4 | All Future Work |
| Language & Editorial | BEV-071 – BEV-077 | 7 | All Accepted |
| **Total** | **BEV-001 – BEV-077** | **77** | |

### Status Totals
| Status | Count |
|---|---|
| Accepted | 53 |
| Under Review | 18 |
| Rejected | 0 |
| Future Work (distinct from Accepted) | 6 |

---

---

## Section 11 — Glass Box D4: Additive Evidence Framework

*Entries BEV-078 through BEV-081 seed the D4 ("additive MOAT") dimension of the Glass Box program (TASK-179). Source: "Food additives 1" research document (New Batch, 2026-06-06), which synthesizes EFSA/JECFA/FDA regulatory evaluations across nine additive classes. All entries are pre-activation: annotate_only entries inform the annotation layer only; score_moving_pending_d7 entries are candidates for a scored rule but require a separate owner D7 sign-off before any rule is written or deployed. The EDPG firewall applies: these entries calibrate the D4 library; no external value feeds a live score path directly. Per-person ADI × bodyweight intake logic is explicitly excluded (BEV-001; BEV-003e — Bari describes the food, not the eater).*

### BEV-078
**Topic:** D4 Tier 1 — Sulfites (E220–228): dose-independent sensitivity population  
**Summary:** Sulfites (sulfur dioxide and sulfite salts, E220–228) are the sole Tier 1 additive class in the reference framework. EFSA (2022) found that estimated intakes for high consumers — especially children — may approach unsafe levels based on a margin-of-exposure analysis; no ADI was established, with EFSA instead setting MOE benchmarks. The primary concern is dose-independent sensitivity: sulfites trigger bronchospasm in asthmatics and destroy thiamine (vitamin B1) in foods. The sensitivity population is defined by the physiological characteristic (asthma), not by intake volume, which distinguishes this from standard ADI exceedance logic. EU labelling requires disclosure ("contains sulfites") at concentrations above 10 mg/kg.  
**Primary source:** Research doc "Food additives 1" (2026-06-06), citing EFSA (2022) sulfite re-evaluation [ref: 35†L310–L318; 35†L319–L324]; EFSA Panel opinion primary  
**Hebrew annotation (consumer-facing):** "מכיל סולפיטים — חומר משמר שמופיע בפירות יבשים, יינות ומוצרים מותססים. מוכר כגורם תגובות אצל אנשים עם אסתמה."  
**Status:** `score_moving_pending_d7` — candidate for a scored rule in D4; activation requires owner D7 sign-off. A separate rule proposal with D7 co-sign must precede any engine implementation. This entry does not authorize any scoring change.  
**Impact:** Future Work (D4), Interpretation  
**Task:** TASK-193

---

### BEV-079
**Topic:** D4 Tier 2 — Azo synthetic colorants (E102, E110, E122, E124, E129): hyperactivity signal in sensitive children  
**Summary:** Synthetic azo dyes — tartrazine (E102), Sunset Yellow (E110), Allura Red (E129), and related — carry a Tier 2 classification due to established hypersensitivity and neurobehavioral signals. The Southampton study (McCann 2007) found that mixtures of six artificial colors plus benzoate modestly increased hyperactivity in a general-child cohort. EFSA's re-evaluation (2008) acknowledged "limited evidence of a small effect in some children" and retained ADIs (tartrazine 7.5 mg/kg, Sunset Yellow 5 mg/kg, Allura Red 7 mg/kg) while requiring EU labelling of six specific dyes with the phrase "may have an adverse effect on activity and attention in children." This is a dose-independent sensitivity population signal (sensitive children), not a general-population toxicity signal. No genotoxic or carcinogenic risk was found at permitted uses. Note: these colorants are label-observable by E-number or common name and are candidates for D4 annotation or scoring.  
**Primary source:** Research doc "Food additives 1" (2026-06-06), citing McCann et al. 2007 Southampton study [ref: 44†L272–L281]; EFSA colorant re-evaluations (2008) primary  
**Hebrew annotation (consumer-facing):** "מכיל צבעי מאכל סינתטיים (כגון טרטרזין E102, צהוב שקיעה E110, אדום אלורה E129). באירופה נדרשת אזהרה: 'עשוי להשפיע על הפעילות והקשב בילדים.'"  
**Status:** `score_moving_pending_d7` — candidate for a scored rule in D4 targeting label-observable azo dyes; activation requires owner D7 sign-off. This entry does not authorize any scoring change.  
**Impact:** Future Work (D4), Interpretation  
**Task:** TASK-193

---

### BEV-080
**Topic:** D4 Tier 3 — Neutral additive classes (flavor enhancers, sorbates, propionates, most polyols, acidity regulators)  
**Summary:** Tier 3 covers additives with no significant human health concerns at regulated doses and no established sensitive-population signal of the kind seen in Tiers 1–2. Representative members: MSG (E621) and disodium nucleotides — JECFA "ADI not specified," no credible harm in RCTs; potassium sorbate (E202) — EFSA ADI 11 mg/kg (as sorbic acid), no specific human hazard; propionates — ADI ~10 mg/kg, no red flags; sorbitol/xylitol/mannitol (polyols) — "ADI not specified," GI effects only at excess intake with EU laxative-effect label required; citric acid (E330), malic acid, phosphoric acid (E338) — "ADI not specified" for most; phosphoric acid Tier 3 at food levels (some bone-density association at very high cola consumption, mixed evidence). Consumer-facing annotation for Tier 3 additives is informational: identity and function, no concern language.  
**Primary source:** Research doc "Food additives 1" (2026-06-06), synthesizing EFSA, JECFA, FDA evaluations across flavor enhancers, sorbates, polyols, and acidity regulators  
**Hebrew annotation (consumer-facing):** "מכיל תוספי מזון מדרגה ניטרלית (כגון E621 גלוטמט, E202 סורבט, חומצה ציטרית E330). מאושרים על ידי גורמי הרגולציה ואין להם חשש מוכח בכמויות המצויות במזון."  
**Status:** `annotate_only` — Tier 3 additives are candidates for identity + function annotation in D4; they are not candidates for a score-moving rule under current evidence. Emulsifier evidence (Tier 2 sub-entries P80/CMC/carrageenan — see BEV-081) is handled separately as the weaker side of Tier 2.  
**Impact:** Future Work (D4), Interpretation  
**Task:** TASK-193

---

### BEV-081
**Topic:** D4 Tier 4 / Emulsifier boundary — beneficial or weak-signal additives (lecithin, natural colors, some stabilizers; P80/CMC/carrageenan annotate-only)  
**Summary:** Two distinct sub-groups are combined here. First, Tier 4 (beneficial or context-dependent): lecithin (E322) — "ADI not specified," provides choline and fatty acids, EFSA no safety concern; natural colorants (beta-carotene E160a, anthocyanins) — "ADI not specified," nutrient-value context; bicarbonates (E500) — leavening, well tolerated; pectin (E440), xanthan (E415) — fiber-like, safe. Second, the emulsifiers P80 (polysorbate-80, E432), CMC (carboxymethylcellulose, E466), and carrageenan (E407): the research doc assigns these Tier 2 in its internal classification, but the 2026 RCT (60 adults, placebo-controlled) found that supplementing a low-emulsifier diet with single emulsifiers lowered fecal short-chain fatty acids but did NOT raise markers of gut inflammation, LPS, or metabolic risk markers. Evidence is rated C (limited) — mostly animal and mechanistic. No direct human pathology from typical emulsifier intake has been demonstrated. Carrageenan modestly increased intestinal permeability in one RCT. On this basis: P80, CMC, and carrageenan are annotate-only — the evidence is suggestive but not directional enough for a scored rule. EFSA permits all three under specified uses.  
**Primary source:** Research doc "Food additives 1" (2026-06-06), citing 2026 RCT [ref: 19†L63–L71]; Chassaing et al. mouse studies [ref: 11†L380–L388]; EFSA evaluations for E322, E407, E432, E466  
**Hebrew annotation (consumer-facing, P80/CMC/carrageenan):** "מכיל מתחלבים (פוליסורבט 80, CMC, קרגינן). מחקרים בבעלי חיים הצביעו על השפעות על המיקרוביום; בניסוי אנושי מבוקר לא נמצאה עלייה בדלקת. נמצאים בבחינה מדעית מתמשכת."  
**Hebrew annotation (consumer-facing, Tier 4 beneficial):** "מכיל לציטין (E322) — חומר טבעי המספק כולין; או צבעים טבעיים (בטא-קרוטן, אנתוציאנינים) — עם ערך תזונתי הקשרי."  
**Status:** `annotate_only` for all sub-groups in this entry. P80/CMC/carrageenan are explicitly NOT score-moving: the 2026 RCT showed ↓SCFA but no rise in inflammation markers; evidence is weak and non-directional. Tier 4 additives (lecithin, natural colors, pectin) are informational annotation only. No evidence conditions are met for a D4 scored rule in this group.  
**Impact:** Future Work (D4), Interpretation  
**Task:** TASK-193

---

## Section 12 — Glass Box D1: Energy Density Signal

*Entry BEV-082 formalizes Dietary Energy Density (DED) as a candidate D1 signal. Source: "Beyond Nutrients: A Systematic Review of Dietary Patterns, Microbial Ecology, and Chronic Disease Outcomes" (New Batch, 2026-06-06). Status: score_moving_pending_d7 — requires owner D7 sign-off before activation. No existing published score is changed.*

### BEV-082
**Topic:** Dietary Energy Density (DED) <1.5 kcal/g as a positive D1 signal  
**Summary:** DED is defined as kilocalories per gram of food as consumed. The research base establishes three distinct findings: (1) A 1-year randomized clinical trial in obese women (ad libitum, no calorie limits) showed that the reduced-fat + fruit/vegetable group (RF+FV) reduced DED more, consumed a greater food weight, and lost significantly more weight than the reduced-fat group alone — with significantly less hunger throughout. (2) A prospective cohort study of postmenopausal women in the WHI found that higher baseline DED was associated with a statistically significant increased risk of developing any obesity-related cancer (breast, colorectal, ovarian, endometrial), and notably this risk was present even in normal-weight women — suggesting DED drives metabolic dysfunction independently of adiposity. (3) The WHI WHEL randomized trial found that the intervention group reduced DED and achieved modest significant weight loss at year 1, though the effect was not sustained at year 5 without broader behavioral strategies. DED is directly computable from the nutrition panel (kcal ÷ serving mass in grams) without any per-person parameters — it describes food architecture, not the eater. This is fully consistent with Bari's de-moralized stance (BEV-008). Proposed thresholds: ≤1.5 kcal/g = positive D1 signal; >2.5 kcal/g = penalized. Category applicability differs substantially: bread and snacks operate in a range where DED is meaningful; dairy (milk, yogurt) is already calibrated to calorie density thresholds and the interaction with DED must be examined to avoid double-counting with existing BEV-043/BEV-044 rules. Single-ingredient whole foods (BEV-050/BEV-051 floor rules) must not be negated by DED signals. Fermentation/live cultures and intact-grain protein kinetics are separately documented in EV-024 and BEV-023 respectively; those signals do not require new rules here — fermented-food claims that appear on dry products (e.g., "fermented" on a cracker) remain annotation-only, not a positive scoring signal, because the structural benefit of live fermentation is absent post-drying.  
**Primary sources (from research doc):** (a) 1-Year DED Trial — randomized parallel weight-loss trial, obese women, RF vs RF+FV ad libitum (RF+FV reduced DED more, greater food weight, less hunger, more weight loss); (b) WHI DED Cohort Study — prospective cohort, postmenopausal US women, highest DED quintile associated with increased risk of obesity-related cancers, limited to normal-weight women; (c) WHI WHEL Trial — randomized dietary intervention, breast cancer survivors, intervention reduced DED at year 1 and year 4, small significant weight loss at year 1 (not sustained at year 4)  
**Status:** `score_moving_pending_d7` — D7 brief drafted at `C:\Bari\01_framework\glass_box_d1_ded_d7_brief_v1.md`. Requires owner D7 sign-off before any scoring rule is activated. No existing published score is changed by this entry.  
**Impact:** Future Work (D1/Glass Box), Scoring (pending D7), Interpretation  
**Task:** TASK-194

---

## Section 13 — Olive Oil D5/D6 Authenticity Signals

*Entry BEV-083 formalizes Turkish-origin as a D6 confidence qualifier annotation signal for the olive oil category. Source: Global Food Fraud and Authenticity research doc (peer-reviewed synthesis, New Batch, 2026-06-06). Status: annotate_only — does not move any D1–D4 score. Owner-approved 2026-06-06. Reclassified D5→D6 on owner review 2026-06-06.*

### BEV-083
**Topic:** Turkish-origin olive oil as a D6 confidence qualifier annotation signal
**Summary:** Peer-reviewed food fraud surveillance research documents Turkey as a high-prevalence origin for adulterated or non-conforming olive oil in international trade. Multiple published surveillance datasets identify Turkish-origin oil as carrying a statistically elevated rate of non-conforming findings (including seed-oil dilution, grade misrepresentation, and geographic mislabeling) relative to other major origin countries. This is a population-level statistical finding across surveillance studies — it is not a per-product laboratory determination and does not assert that any individual product bearing Turkish origin is adulterated. Bari uses this signal as a D6 confidence qualifier: products where `olive_harvest_country = "TR"` receive the `origin_turkey` annotation (derived field: `d6_origin_traceability_qualifier`), surfaced in the D6 expansion drawer with approved factual Hebrew consumer copy. The annotation qualifies Bari's confidence in the origin claim rather than asserting a transparency gap (the origin IS stated on the label — no disclosure failure exists). The annotation does not constitute a product-quality judgment, an accusation, or a safety recommendation. Signal does not interact with D1–D4 scoring paths. Evidence tier: B (Moderate) — consistent directional finding across published surveillance literature; methodology is observational and relies on market-sample testing programs, which have known sampling limitations. Owner-approved 2026-06-06 as a reliable source for annotation purposes.
**Source:** Global Food Fraud and Authenticity research doc (New Batch, 2026-06-06; peer-reviewed synthesis); owner directive 2026-06-06 confirming source reliability and approving Turkish-origin as an annotation signal; reclassified D5→D6 on owner review 2026-06-06.
**Status:** Accepted — `annotate_only`
**Impact:** Interpretation (D6 confidence qualifier, olive oil category)
**Task:** TASK-197

---

## Registry Summary (updated)

| Section | ID Range | Count | Notes |
|---|---|---|---|
| Core Framework & Philosophy | BEV-001 – BEV-010 | 10 | All Accepted |
| Scoring Architecture | BEV-011 – BEV-020 | 10 | BEV-020 Under Review |
| Processing Science Positions | BEV-021 – BEV-031 | 11 | BEV-026 Under Review |
| Nutritional Science Positions | BEV-032 – BEV-040 | 9 | BEV-036 Under Review |
| Category Calibrations | BEV-041 – BEV-048 | 8 | All Accepted |
| Hard Cap & Floor Rules | BEV-049 – BEV-053 | 5 | BEV-053 Under Review |
| Product-Level Rulings | BEV-054 – BEV-061 | 8 | Mixed |
| Known Distortions | BEV-062 – BEV-066 | 5 | All Under Review |
| Future Architecture | BEV-067 – BEV-070 | 4 | All Future Work |
| Language & Editorial | BEV-071 – BEV-077 | 7 | All Accepted |
| Glass Box D4: Additive Evidence | BEV-078 – BEV-081 | 4 | score_moving_pending_d7 (BEV-078, BEV-079); annotate_only (BEV-080, BEV-081) |
| Glass Box D1: Energy Density | BEV-082 | 1 | score_moving_pending_d7 |
| Olive Oil D5/D6 Authenticity | BEV-083 | 1 | annotate_only; reclassified D5→D6 2026-06-06 |
| **Total** | **BEV-001 – BEV-083** | **84** | |

### Status Totals
| Status | Count |
|---|---|
| Accepted | 54 |
| Under Review | 18 |
| Rejected | 0 |
| Future Work (distinct from Accepted) | 6 |
| score_moving_pending_d7 | 4 |
| annotate_only | 2 |

---

---

## Section 14 — Juice NOVA-1 Floor Gate (TASK-217)

*Entry BEV-084 governs the three-condition gate on the `nova1_single_ingredient` floor for the `beverage / juice_100` sub-category. D7-approved by Nutrition Agent + Product Agent, 2026-06-07. Source: accepted food science on concentration/reconstitution as a processing step materially distinct from fresh-pressing.*

### BEV-084
**Topic:** NOVA-1 single-ingredient floor gate for reconstituted-from-concentrate juice (juice_100 category)
**Summary:** The `nova1_single_ingredient` floor (NOVA1_SINGLE_FLOOR = 85, score lifted to A) was designed for genuine single-ingredient whole foods — nuts, plain fruit, cold-pressed juice — where the engine's penalty architecture would incorrectly penalise natural composition. Reconstituted-from-concentrate juice is a structurally distinct processing step: water removal by heat evaporation drives volatile loss (aromatic compounds, heat-labile vitamin C fractions), followed by water re-addition. Published food science consistently documents that this cycle (a) destroys a portion of heat-labile phytochemicals, (b) alters flavonoid and polyphenol bioavailability profiles, and (c) modifies the product's sensory and enzymatic profile relative to cold-pressed or freshly squeezed equivalents — even when macronutrient panels (sugar, calories, protein) converge. This is not a health claim; it is a structural-processing classification consistent with BSIP2's NOVA 3 assignment for reconstituted-from-concentrate products. The floor was not designed to benefit NOVA 3 products, and its mis-application to unlabelled reconstituted juice (where reconstitution markers are present in ingredient text but NOVA inference did not fire NOVA 3) produces a category A score (85) on a product whose weighted dimension score may be as low as 57–58. The gate conditions below close this gap. Evidence tier: Moderate (well-established food science; volatile and phytochemical loss in juice concentration is documented in peer-reviewed food chemistry literature; no RCT is required or applicable for a processing-classification rule). Label observability: all three conditions are extractable from observable label data (BSIP1 `nova_proxy` field, BSIP1 `has_fruit_concentrate` enrichment flag when present, and direct ingredient-text substring matching for Hebrew and English reconstitution markers — no per-person parameters required).

**Gate rule (ALL three conditions must be satisfied for floor to fire):**
1. `nova_proxy == 1` (floor was triggered)
2. `has_fruit_concentrate == false` (BSIP1 enrichment flag; when absent, derived from condition 3)
3. Ingredient text does NOT contain any of: `רכז`, `משוחזר`, `מרוכז`, `concentrate`, `from concentrate`

**If any condition fails:** floor does not fire; `nova_proxy` is set to minimum 2; product is subject to existing NOVA 2/3 caps. No other scoring logic changes.

**Scope:** `beverage / juice_100` sub-category only. Other categories (whole_food_fat, dairy, etc.) with NOVA 1 single-ingredient floors are unaffected.

**Category scope guard:** `juice_100_floor_gate_active` flag — only active when `category == "beverage"` and product has `juice_subpool == "juice_100"` OR is routed as a single-ingredient beverage. Guard prevents blast-radius to other beverage sub-types.

**Scientific basis:** Heat-driven volatile loss in juice concentration (documented); altered phytochemical and flavonoid profiles in reconstituted vs. fresh-pressed juice (documented); enzymatic changes from pasteurisation required post-reconstitution (documented). These are L2/L3-level structural-processing facts, not individual dietary predictions.

**Evidence tier:** Moderate (B) — consistent directional finding in peer-reviewed food chemistry; no RCT applicable; mechanistic basis is robust.

**Status:** Accepted — `score_moving` (implemented TASK-217, 2026-06-07). D7 co-sign: Nutrition Agent + Product Agent.

**Implementation:** `03_operations/bsip2/proto_v0/src/score_engine.py`, `apply_floors()`, three-condition gate block (TASK-217 / BEV-084).

**Impact:** Scoring (juice_100 category)

**Task:** TASK-217

---

## Registry Summary (updated)

| Section | ID Range | Count | Notes |
|---|---|---|---|
| Core Framework & Philosophy | BEV-001 – BEV-010 | 10 | All Accepted |
| Scoring Architecture | BEV-011 – BEV-020 | 10 | BEV-020 Under Review |
| Processing Science Positions | BEV-021 – BEV-031 | 11 | BEV-026 Under Review |
| Nutritional Science Positions | BEV-032 – BEV-040 | 9 | BEV-036 Under Review |
| Category Calibrations | BEV-041 – BEV-048 | 8 | All Accepted |
| Hard Cap & Floor Rules | BEV-049 – BEV-053 | 5 | BEV-053 Under Review |
| Product-Level Rulings | BEV-054 – BEV-061 | 8 | Mixed |
| Known Distortions | BEV-062 – BEV-066 | 5 | All Under Review |
| Future Architecture | BEV-067 – BEV-070 | 4 | All Future Work |
| Language & Editorial | BEV-071 – BEV-077 | 7 | All Accepted |
| Glass Box D4: Additive Evidence | BEV-078 – BEV-081 | 4 | score_moving_pending_d7 (BEV-078, BEV-079); annotate_only (BEV-080, BEV-081) |
| Glass Box D1: Energy Density | BEV-082 | 1 | score_moving_pending_d7 |
| Olive Oil D5/D6 Authenticity | BEV-083 | 1 | annotate_only; reclassified D5→D6 2026-06-06 |
| Juice NOVA-1 Floor Gate | BEV-084 | 1 | score_moving; D7 co-signed 2026-06-07; TASK-217 |
| **Total** | **BEV-001 – BEV-084** | **85** | |

### Status Totals
| Status | Count |
|---|---|
| Accepted | 55 |
| Under Review | 18 |
| Rejected | 0 |
| Future Work (distinct from Accepted) | 6 |
| score_moving_pending_d7 | 4 |
| annotate_only | 2 |
| score_moving (implemented) | 1 |

---

## Section 15 — Emulsifier Identity Deltas (TASK-222A)

*Entry BEV-085 governs the TASK-222A activation of F1 identity deltas (`ADDITIVE_IDENTITY_DELTAS` in constants.py) and retirement of the sprint1 +2/−1 additive-count corrections. Source: BSIP2 research review batch (2026-06-09), synthesizing human RCT evidence for carrageenan/CMC gut-barrier effects, commercial DIAAS data for protein-bar matrix discount, and FDA regulatory status for BHA/E320.*

### BEV-085
**Topic:** Emulsifier identity-based scoring — carrageenan/CMC/P80 penalty (−3 each, cap −6) and lecithin relief (+2) via F1 identity deltas
**Summary:** The sprint1 EV-003/019 system used a coarse additive-count correction (+2 for high-risk emulsifiers, −1 for lecithin-only) as a proxy until per-ingredient identity signals were available. TASK-133A's ingredient taxonomy now supplies exact identity resolution. Three evidence streams support the transition:
- **Carrageenan/CMC (human RCT):** A placebo-controlled human feeding study (2023) found that carrageenan (∼250 mg/day) increased gut permeability (lactulose/mannitol ratio) vs placebo, and CMC (∼15 g/day for 11 days) reduced fecal SCFAs and altered the microbiome. These are the first human RCT data for food-relevant doses directly measuring gut-barrier effects. Evidence tier: Strong (A) for carrageenan/CMC — human placebo-controlled RCT, food-relevant dose, direct endpoint. Polysorbate-80 remains mechanistic/animal only — evidence tier: Moderate (B).
- **Lecithin (regulatory consensus):** Soy/sunflower lecithin (E322) has a well-established safety profile (GRAS, EFSA acceptable intake not specified). It is a naturally occurring phospholipid emulsifier. The +2 relief reflects its benign status — less penalizing than the sprint1 full count-exclusion (−18 base) but still marking it as an additive (unlike native starch which is fully excluded).
- **Cap rationale:** The −6 cap ensures that even a product with 3+ high-risk emulsifiers never has additive_quality reduced by more than 6 points from this rule alone. This is bounded by the existing ADDITIVE_FAMILY_BUDGET which already limits total additive_quality loss.
**Evidence tier:** Strong (A) for carrageenan/CMC human RCT; Moderate (B) for P80 (mechanistic only); Regulatory consensus for lecithin (not human RCT).
**Label observability:** Fully observable. `tax_emulsifier_concern` and `tax_emulsifier_benign` are extracted from ingredient text via ingredient_taxonomy.py resolution. The sprint1 detection functions (lexical patterns for Hebrew and E-numbers) remain for traceability/rollback.
**Status:** Accepted — score_moving (implemented TASK-222A, 2026-06-09). Replaces retired sprint1 EV-003/019 additive-count corrections.
**Implementation:** `03_operations/bsip2/proto_v0/src/constants.py` — `ADDITIVE_IDENTITY_DELTAS` values set non-zero; `03_operations/bsip2/proto_v0/src/signal_extractor.py` — sprint1 corrections retired to zero; `03_operations/bsip2/proto_v0/src/score_engine.py` — `_identity_additive_deltas()` now active.
**Impact:** Scoring (additive_quality dimension — processed categories)
**Task:** TASK-222A

---

*Entry BEV-086 governs the TASK-222B activation of F2 protein-bar matrix discount (`PROTEIN_QUALITY_MATRIX_DISCOUNT` in constants.py). Source: BSIP2 research review batch (2026-06-09), synthesizing commercial DIAAS data for bar-matrix protein bioavailability reduction. Same batch as BEV-085 (emulsifier deltas) and planned BEV-087 (BHA/E320).*

### BEV-086
**Topic:** Protein-bar matrix discount — reconstructed-protein quality penalty (×0.80) for bar-format isolates and collagen (×0.55) for any format
**Summary:** The BSIP2 scoring engine has a documented structural gap: bar-format products using reconstructed protein isolates (whey/soy/pea/egg/casein isolate) receive full protein-quality credit even though the bar matrix reduces amino-acid bioavailability by 47–81% relative to isolated protein (DIAAS measurements, commercial study). Collagen is additionally discounted because it is an incomplete protein (lacks tryptophan) with the lowest matrix DIAAS. Two discount tiers:
- **Reconstructed (×0.80):** Bar-format isolate products in `snack_bar_granola` category. Midpoint of the 47–81% DIAAS band — conservative, does not assume the worst-case reduction. Scoped to bar-format only to PROTECT in-context whey isolate (protein puddings, Greek yogurt with whey concentrate — not bar-format, unchanged).
- **Collagen (×0.55):** Any product where collagen peptides appear in the primary ingredient window (position ≤ 3). Incomplete AA profile (no tryptophan) and lowest matrix DIAAS. Applies regardless of category.
**Evidence tier:** Moderate (B) — commercial DIAAS data, directionally consistent with known matrix effects, but single-source and not yet independently replicated in peer-reviewed literature at bar-relevant DIAAS scale. Conservative midpoint values mitigate over-penalization risk.
**Label observability:** Fully observable. `protein_matrix_form` extracted from ingredient text primary window (positions 1–3) via `RECONSTRUCTED_PROTEIN_MARKERS_HE` and `COLLAGEN_MARKERS_HE` in signal_extractor.py. Excludes milk powder (verified false-positive source: milk-powder chocolate/cereal bars must not trigger the discount).
**Status:** Accepted — score_moving (implemented TASK-222B, 2026-06-09). Corpus impact: 0 non-zero score deltas (2 products with reconstructed form, both 0g protein; 0 collagen products).
**Implementation:** `03_operations/bsip2/proto_v0/src/constants.py` — `PROTEIN_QUALITY_MATRIX_DISCOUNT` activated (DEC-004 placeholder values confirmed); `03_operations/bsip2/proto_v0/src/score_engine.py` — `score_protein_quality()` uses discount on quality score only.
**Impact:** Scoring (protein_quality dimension — snack_bar_granola category for reconstructed, any category for collagen)
**Task:** TASK-222B

---

*Entry BEV-087 governs the TASK-222C confirmation of F4 BHA named penalty (E320). Source: BSIP2 research review batch (2026-06-09), FDA reassessment RFI (2026-02-10), NTP listing. Same batch as BEV-085/086.*

### BEV-087
**Topic:** BHA/E320 named penalty — regulatory-transparency flag on additive_quality (−5) for Butylated hydroxyanisole
**Summary:** FDA launched a post-market reassessment of BHA (E320) on 2026-02-10 (RFI closed 2026-04-13); no final GRAS rule has landed as of 2026-06. NTP lists BHA as "reasonably anticipated to be a human carcinogen." The penalty is a small regulatory-transparency flag, not a health-risk score — distinct from the generic antioxidant-category count (which BHA, BHT and benign tocopherol currently share). BHT (E321) is explicitly differentiated: NOT under FDA reassessment, no penalty.
- **Synonym gap fix (TASK-222C):** The ingredient taxonomy had `E320` and `E 320` as BHA synonyms but not `E-320` (hyphen form). Bread light products use `E-320` in ingredient text. TASK-222C adds `"E-320"` to BHA synonyms and `"E-321"` to BHT synonyms for data-consistency.
- **Corpus prevalence (TASK-222C scan):** 2/1,357 products (0.15%) across all BSIP1 runs — both in bread light corpus (`run_bread_light_001`). Near-zero prevalence; no scoring sprint warranted. The penalty was always structurally live at -5; TASK-222C confirms the magnitude and fixes the taxonomy gap.
**Evidence tier:** Regulatory (FDA RFI + NTP listing) — not a human RCT tier. Appropriate for a small transparency flag, not a major scoring driver.
**Label observability:** Fully observable. `tax_bha_present` extracted via `ingredient_taxonomy.resolve_additive()` matching Hebrew/E-number synonyms. `E-320` variant now included (TASK-222C).
**Status:** Accepted — score_moving (code was always live; TASK-222C fixes taxonomy gap). Corpus impact: 2 products affected (−5 additive_quality; net −3 after lecithin relief).
**Implementation:** `03_operations/bsip2/proto_v0/src/constants.py` — `BHA_NAMED_PENALTY=5` confirmed; `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py` — `"E-320"` and `"E-321"` synonyms added; `03_operations/bsip2/proto_v0/src/score_engine.py` — `_identity_additive_deltas()` already applied penalty on `tax_bha_present`.
**Impact:** Scoring (additive_quality dimension — any category with BHA-bearing products; currently bread light only)
**Task:** TASK-222C

---

*End of Evidence Registry v1. Next BEV entry: BEV-088.*
