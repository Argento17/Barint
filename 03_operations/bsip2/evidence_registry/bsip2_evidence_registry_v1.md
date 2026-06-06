# BSIP2 Evidence Registry v1

**Classification:** Internal — Scoring Intelligence  
**Version:** 1.0  
**Date:** 2026-05-30  
**Owner:** Chief Nutrition Officer  
**Source document:** Engineering Architecture for AI-Driven Food and Supplement Intelligence (78pp)  
**Scope:** BSIP2 packaged food engine only. Section 2 (Supplement Engine) is explicitly excluded.

---

## Registry Structure

| Section | Contents |
|---------|----------|
| A — Primary Findings | 20 evidence findings with full field extraction |
| B — Guardrails | 20 nutrition misconceptions that must NOT be modeled |
| C — Do-Not-Model-Yet | 20 high-uncertainty domains deferred from algorithmic treatment |
| D — Roadmap | Ranked implementation queue |

**Core constraint on all findings:** Only signals observable or inferrable from packaged food labels (ingredients list, nutrition panel, product format, processing claims) are eligible for `should_affect_score_now: true`.

---

## Section A — Primary Findings

---

### EV-001 — Siga / MUP Five-Tier Processing Classification

| Field | Value |
|-------|-------|
| **finding_id** | EV-001 |
| **concept** | Siga multi-tier ultra-processing classification replacing binary NOVA 4 |
| **scientific_rationale_short** | NOVA 4 is a single bucket treating fortified whole-grain cereals identically to hyper-palatable confectionery. Siga subdivides NOVA 4 into C0.1, C0.2, and C1–C3 using Marker of Ultra-Processing (MUP) counts and risk levels. MUP1 = chemically synthesized but nature-identical (starches, natural flavourings). MUP2 = artificially synthesized (synthetic aromas). At-risk = EFSA/IARC-scrutinized additives. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — BSIP2's current NOVA proxy uses a single Group 4 classification that produces scoring errors for processed-but-nutritious products. Siga granularity corrects this. |
| **implementation_complexity** | High |
| **recommended_action** | implement_now |
| **affected_categories** | All categories; highest impact: cereals, snack_bars, dairy_protein, sauce_spread |
| **candidate_signal_name** | `siga_processing_intensity`, `mup_density_score` |
| **should_affect_score_now** | false — requires MUP taxonomy dictionary and ingredient-to-tier mapping engine before scoring can use this |
| **required_input_fields** | `ingredients_list`, `extracted_additives` |
| **risk_of_misuse** | Over-penalising processed-but-nutritious foods if MUP1 (nature-identical) items are treated as equivalent to MUP2 (synthetic) items |
| **notes** | Prerequisite for EV-002. The Siga threshold rules (sugar >12.5g/100g, fat >17.5g/100g, salt >0.75g/100g) interact with MUP count to set tier. Implement taxonomy dictionary first; scoring second. |

```yaml
study_objects:
  - claim: "NOVA 4 ultra-processed food classification is associated with adverse health outcomes at population level, independent of nutrient content"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: B
    source_doi: "10.1136/bmj.k322"
    notes: "Monteiro et al. 2018 NovaStar cohort; large observational study underpinning NOVA as a classification system. dose_realistic: true (dietary exposure level). population_direct: true (general adult population). Tier B rather than A: observational design means causation cannot be established; NOVA classification introduces inter-rater variability for borderline products. The Siga sub-classification (EV-001) addresses the limitation that NOVA 4 is too coarse — it is an extension, not a replacement."
  - claim: "Siga MUP-based sub-classification of ultra-processed foods improves discrimination between high-risk and lower-risk NOVA 4 products"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: B
    source_doi: "internal:bsip2_evidence_registry_v1.md"
    notes: "The Siga methodology is documented in peer-reviewed form (Pointereau et al., Nutrients 2020) but the specific discriminative validity for health outcomes has limited direct RCT evidence — the classification is mechanism-based. Tier B reflects that the biological rationale is strong and the classification is regulatory-agency-anchored (EFSA/IARC at-risk lists), but population-level outcome confirmation of the sub-tiers specifically is limited."
```

---

### EV-002 — At-Risk Additive Count (MUP Category)

| Field | Value |
|-------|-------|
| **finding_id** | EV-002 |
| **concept** | Enumeration of additives classified as high-risk by EFSA or IARC |
| **scientific_rationale_short** | Siga's "At-risk additives" are a defined subset of MUPs that regulatory panels have flagged for ongoing safety evaluations. These are distinct from the broader additive category. Counting them enables additive risk to scale with formulation severity rather than a binary additive-present/absent penalty. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — replaces the current all-additive-equal penalty with a risk-weighted count. A product with 1 at-risk additive is categorically different from one with 5. |
| **implementation_complexity** | High |
| **recommended_action** | implement_now |
| **affected_categories** | All; highest priority: snack_bars, sauce_spread, cereal_system, dairy_protein |
| **candidate_signal_name** | `at_risk_additive_count` |
| **should_affect_score_now** | false — requires a maintained at-risk additive reference list mapped to Hebrew ingredient terms |
| **required_input_fields** | `ingredients_list`, `extracted_additives` |
| **risk_of_misuse** | Regulatory lists change; a frozen v1 list risks penalising since-cleared additives or missing newly flagged ones |
| **notes** | The at-risk list is a maintenance obligation. Must be versioned alongside BSIP2 releases. Differentiate clearly from MUP1/MUP2 in implementation. |

---

### EV-003 — Emulsifier Risk Differentiation

| Field | Value |
|-------|-------|
| **finding_id** | EV-003 |
| **concept** | CMC (E466) and Polysorbate 80 (E433) cause measurable gut barrier disruption; soy/sunflower lecithin (E322) and gum arabic do not |
| **scientific_rationale_short** | Controlled human trial confirmed CMC reduces Faecalibacterium prausnitzii and Akkermansia muciniphila while lowering SCFA. P80 promotes pro-inflammatory Proteobacteria and thins mucosal lining causing bacterial translocation. Carrageenan (E407) disrupts tight junctions via ZO-1 protein. By contrast, soy lecithin demonstrated minimal microbiota impact in ex vivo studies, and gum arabic serves as a prebiotic bifidogenic substrate. |
| **evidence_strength** | Strong (CMC, P80); Moderate-Strong (carrageenan); Moderate (lecithin safety) |
| **confidence_level** | High |
| **BSIP2_relevance** | Critical — current BSIP2 applies undifferentiated emulsifier penalties. This finding supports a tiered emulsifier scoring model: high-risk (CMC, P80, carrageenan), neutral (soy/sunflower lecithin), prebiotic (gum arabic). |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | All; highest density: snack_bars, dairy_protein, sauce_spread, beverage |
| **candidate_signal_name** | `mucus_thinning_emulsifier_load` |
| **should_affect_score_now** | true — ingredient text matching is sufficient; no nutrition panel data required |
| **required_input_fields** | `ingredients_list`, `extracted_additives` |
| **risk_of_misuse** | Carrageenan distinction (food-grade vs degraded poligeenan) cannot be resolved from labels — apply penalty uniformly per label presence |
| **notes** | Hebrew terms to match: קרבוקסי מתיל צלולוז, CMC, E466 (CMC); פוליסורבט 80, E433 (P80); קרגינן, E407 (carrageenan); לציטין סויה, לציטין חמניות, E322 (exempt); גומי ערבי (prebiotic exempt). |

```yaml
study_objects:
  - claim: "Carboxymethylcellulose (CMC/E466) consumption disrupts the gut microbiota, reducing Faecalibacterium prausnitzii and short-chain fatty acids"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: A
    source_doi: "10.1016/j.cell.2021.12.019"
    notes: "Chassaing et al. 2022 — controlled human feeding trial (n=16, crossover). CMC at doses achievable from typical ultra-processed food consumption (approximately matching daily label exposure in a Western diet). Population: healthy adults. This is the foundational human RCT supporting the Strong tier for CMC. Mechanistic plausibility already established in mouse models by the same group."
  - claim: "Polysorbate 80 (E433) promotes pro-inflammatory gut bacteria and thins the intestinal mucus layer"
    dose_realistic: true
    population_direct: false
    rob_grade: high
    evidence_tier: C
    source_doi: "10.1038/nature14232"
    notes: "Chassaing & Gewirtz 2015 — mouse model demonstrating mucosal thinning and microbiome dysbiosis with P80. dose_realistic: true (concentrations in the study approximate food-use levels). population_direct: false (animal model, not human RCT). The evidence is preclinical; the mechanism is biologically plausible and consistent with in-vitro findings, but the Strong entry-level tier for P80 in the registry reflects the weight of the full literature including the human trial for CMC. This individual study is Tier C."
  - claim: "Soy lecithin (E322) has minimal adverse impact on gut microbiota composition"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: B
    source_doi: "internal:bsip2_evidence_registry_v1.md"
    notes: "Ex vivo and observational evidence; no large controlled human trial. The Moderate exemption for lecithin in the scoring model is based on the absence of the adverse mechanism seen with CMC/P80, supported by ex vivo studies and traditional dietary use. The 'internal' source reflects that the synthesis is based on the BSIP2 evidence document rather than a single primary trial."
```

---

### EV-004 — Allulose Caloric and Glycemic Exemption

| Field | Value |
|-------|-------|
| **finding_id** | EV-004 |
| **concept** | D-Allulose provides 0.4 kcal/g (not 4.0), does not elevate blood sugar or insulin, and is ~70% excreted unchanged |
| **scientific_rationale_short** | Allulose is a C-3 epimer of fructose. It is absorbed in the small intestine but not metabolized into glycogen. Approximately 70% is excreted in urine unchanged; the remaining 30% reaches the colon without contributing glycemic load. FDA has granted it an exemption from the "added sugar" declaration requirement. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — treating allulose as standard sugar in the sugar scoring dimension produces false high-sugar penalties on keto/low-sugar products legitimately formulated with allulose |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | snack_bars, beverage, dairy_protein, sauce_spread (keto-positioned products) |
| **candidate_signal_name** | `allulose_adjusted_sugar_g` |
| **should_affect_score_now** | true — ingredient list text match; apply 90% reduction to allulose contribution in sugar score |
| **required_input_fields** | `ingredients_list`, `extracted_sweeteners`, `normalized_nutrition_per_100g.sugars_g` |
| **risk_of_misuse** | Allulose quantities are not declared on Israeli labels; can only flag presence, not exact grams. Apply a flag + conservative partial credit. |
| **notes** | Long-term large-scale human safety trials are limited. Score adjustment is sound; full caloric recalculation requires quantity — flag-only until quantity is detectable. |

---

### EV-005 — Polyol Osmotic Laxative Threshold

| Field | Value |
|-------|-------|
| **finding_id** | EV-005 |
| **concept** | Sugar alcohols above 10g/serving trigger osmotic laxation; EU/UK law mandates warning label at >10% polyol content |
| **scientific_rationale_short** | Sorbitol, xylitol, erythritol, and maltitol are low-digestible carbohydrates that draw water osmotically into the large intestine. EU regulation requires a laxative effect warning on products with >10% added polyols. The 10g/serving threshold is the clinical trigger for gastrointestinal symptoms in most adults. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — "keto" and "low-carb" products often rely heavily on polyols as sugar replacements. Current BSIP2 does not flag this consumer safety concern. |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | snack_bars, beverage (keto/low-carb positioned) |
| **candidate_signal_name** | `polyol_laxative_potential` |
| **should_affect_score_now** | true — detect polyol presence in ingredient list; flag if multiple polyols or if product is keto/sugar-free |
| **required_input_fields** | `ingredients_list`, `extracted_sweeteners` |
| **risk_of_misuse** | Cannot calculate exact grams from label alone; erythritol has higher individual tolerance than sorbitol. Flag presence + count; do not compute precise osmotic load. |
| **notes** | Hebrew polyol terms: סורביטול, קסיליטול, אריתריטול, מלטיטול, לקטיטול, מניטול, איזומלט. Erythritol is better tolerated than others; consider differentiated risk weights. |

---

### EV-006 — Viscous vs Non-Viscous Soluble Fiber

| Field | Value |
|-------|-------|
| **finding_id** | EV-006 |
| **concept** | Viscous soluble fibers (psyllium, β-glucan) reduce glycemic response by gel formation; non-viscous soluble fibers (inulin, polydextrose) do not |
| **scientific_rationale_short** | Viscous fibers form a thick gel in the GI tract that delays gastric emptying and slows nutrient diffusion, producing measurable postprandial glycemic reduction. Non-viscous soluble fibers (prebiotic fibers like inulin, FOS, polydextrose) undergo colonic fermentation but do not affect glycemic kinetics in the small intestine. Treating them identically produces scoring errors. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Critical — current BSIP2 treats all dietary fiber identically in glycemic scoring. Inulin-fortified products score high-fiber but provide no glycemic dampening. |
| **implementation_complexity** | High |
| **recommended_action** | implement_now |
| **affected_categories** | cereal_system, snack_bars, bread (whole_food categories with fiber claims) |
| **candidate_signal_name** | `viscosity_fiber_ratio`, `viscous_fiber_g` |
| **should_affect_score_now** | false — requires viscous fiber vocabulary dictionary to parse ingredient text reliably |
| **required_input_fields** | `ingredients_list`, `normalized_nutrition_per_100g.dietary_fiber_g` |
| **risk_of_misuse** | Exact viscous fiber quantity is not on the label; presence-only detection risks under-crediting psyllium-dominant products |
| **notes** | Viscous: psyllium husk (קליפת צ'יה, פסיליום), oat beta-glucan (ביתא גלוקן שיבולת שועל), guar gum (גואר). Non-viscous/prebiotic: inulin (אינולין), FOS, chicory root (שורש עולש), polydextrose, resistant dextrin. Implement vocabulary before scoring. |

---

### EV-007 — Intrinsic vs Isolated Fiber Efficacy

| Field | Value |
|-------|-------|
| **finding_id** | EV-007 |
| **concept** | Intrinsic plant fiber retains cellular structure and provides full metabolic benefits; isolated/added fiber does not replicate this |
| **scientific_rationale_short** | Intrinsic fibers remain integrated within plant cell walls with intact physical matrix. Isolated fibers (chicory inulin, resistant maltodextrin, pea fiber isolate) are extracted and added to processed foods. Regulatory bodies require isolated fibers to demonstrate beneficial physiological outcomes, but these do not match the full systemic effects of intact plant matrix fibers. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — "high fiber" claims on processed foods frequently rely on added isolated fibers that don't deliver equivalent metabolic protection. Scoring must discount added fiber vs. whole-food fiber. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now |
| **affected_categories** | cereal_system, snack_bars, bread, dairy_protein (fiber-fortified products) |
| **candidate_signal_name** | `intrinsic_fiber_ratio`, `fiber_source_quality` |
| **should_affect_score_now** | false — requires ingredient parsing to identify isolated fiber additions vs. whole-grain sources |
| **required_input_fields** | `ingredients_list`, `normalized_nutrition_per_100g.dietary_fiber_g`, `extracted_matrix_markers` |
| **risk_of_misuse** | Isolated fiber fortification is difficult to distinguish from whole-grain intrinsic fiber purely from the ingredients list in ambiguous formulations |
| **notes** | Related to EV-009 (intact grain). Isolated fiber signals in ingredient text: inulin, chicory root extract, pea fiber, resistant dextrin, wheat fiber. Whole-grain intrinsic signals: whole wheat flour, rolled oats, bran. Apply a 30–40% efficacy discount to detected isolated fiber sources. |

---

### EV-008 — Liquid vs Solid Matrix Satiety

| Field | Value |
|-------|-------|
| **finding_id** | EV-008 |
| **concept** | Liquid food matrices bypass oral mechanoreceptors and accelerate gastric emptying, producing substantially lower satiety per calorie than solid matrices |
| **scientific_rationale_short** | Liquid matrices fast-track gastric emptying, bypassing the stretch-sensitive vagal afferents that initiate peptide-mediated satiety (PYY, GLP-1, CCK). This is mechanistically established and not nutritionally compensated by equivalent macronutrients in liquid form. High-viscosity liquids can partially mimic solid retention. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — the current `beverage` archetype's strict calorie threshold partially captures this, but the satiety discount for liquid meal replacements and protein shakes is not applied at the satiety dimension level. |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | beverage, dairy_liquid; also: any snack_bar archetype product in liquid/gel format |
| **candidate_signal_name** | `matrix_state_factor` |
| **should_affect_score_now** | true — physical state (liquid vs solid) is inferable from archetype routing and product name |
| **required_input_fields** | `archetype`, `canonical_name_he`, `normalized_nutrition_per_100g.energy_kcal` |
| **risk_of_misuse** | Viscous liquid products (yogurt, kefir, thick smoothies) should not receive the full liquid penalty — apply based on viscosity signals |
| **notes** | Misconception 9 in the source document explicitly calls out the equivalence assumption as algorithmically incorrect. Already partially handled by the beverage calorie density table but not at the satiety signal level. |

---

### EV-009 — Intact Grain / Milling Disruption

| Field | Value |
|-------|-------|
| **finding_id** | EV-009 |
| **concept** | Intact plant cell walls physically insulate starch granules from pancreatic amylase; fine milling destroys this insulation and accelerates glycemic response |
| **scientific_rationale_short** | Plant cell walls contain starch granules that survive cooking and prevent enzymatic access. Industrial milling at high shear destroys this insulation. Steel-cut oats and cracked grains retain this protection; finely milled flour from the same grain does not, producing a substantially higher glycemic response despite identical macronutrient content. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — two products can have identical fiber and carbohydrate values but dramatically different glycemic impact depending on grain processing state. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now |
| **affected_categories** | cereal_system, bread (all grain-based categories) |
| **candidate_signal_name** | `grain_matrix_integrity_score`, `milling_disruption_penalty` |
| **should_affect_score_now** | false — requires ingredient text classification of grain processing state (whole vs milled vs extruded) |
| **required_input_fields** | `ingredients_list`, `extracted_matrix_markers`, `normalized_nutrition_per_100g.dietary_fiber_g` |
| **risk_of_misuse** | "Whole grain" marketing claims do not guarantee low milling disruption — whole grain flour is still fine-milled. Detection should prioritise particle size signals over marketing claims. |
| **notes** | Related to EV-010 (extrusion). Intact grain signals: steel-cut oats, cracked wheat, rolled oats (not instant), groats. Disrupted: "whole wheat flour", "oat flour", extruded grain shapes. The matrix_integrity_framework already exists in BSIP2 — this finding confirms its scientific basis. |

---

### EV-010 — Extrusion Matrix Destruction

| Field | Value |
|-------|-------|
| **finding_id** | EV-010 |
| **concept** | High-shear extrusion physically obliterates natural food matrix, fully gelatinising starch and producing a higher glycemic index than boiled whole grains regardless of macronutrient parity |
| **scientific_rationale_short** | Extrusion uses extreme high-shear, high-temperature, high-pressure processing that destroys crystalline starch structure, denatures proteins, and produces a hyper-bioaccessible, hyper-palatable product. Extruded grain shapes have a higher GI than boiled intact grains of identical macronutrient composition. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — cereal puffs, extruded snack shapes, and textured soy proteins should receive a matrix destruction penalty that standard NOVA processing scores do not fully capture. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now |
| **affected_categories** | cereal_system, snack_bars (puffed/extruded products) |
| **candidate_signal_name** | `extrusion_matrix_penalty` |
| **should_affect_score_now** | true — extruded product signals are detectable from ingredient terms and product name |
| **required_input_fields** | `ingredients_list`, `canonical_name_he`, `extracted_matrix_markers` |
| **risk_of_misuse** | Some healthy products (whole grain puffs) are technically extruded but nutritionally intact — apply penalty to refined-grain extrusion products, not whole-grain puffed forms |
| **notes** | Extrusion signals: פריכית, פצפוצים, חטיף תירס, textured soy protein (נתחי סויה). Paired with EV-009: extrusion is the most severe form of milling disruption. |

---

### EV-011 — Sodium-to-Potassium Ratio

| Field | Value |
|-------|-------|
| **finding_id** | EV-011 |
| **concept** | The sodium-to-potassium ratio is a stronger predictor of stroke and cardiovascular disease than sodium intake in isolation |
| **scientific_rationale_short** | The sodium-potassium pump (Na+/K+-ATPase) is central to cellular electrolyte balance and vascular function. Populations with high Na:K ratio show dose-dependent increased stroke and CVD risk independent of absolute sodium intake. A ratio <1.0 (more potassium than sodium) is associated with protective effects. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Medium — current scoring penalises sodium in isolation. A product with high sodium but even higher potassium should receive reduced cardiovascular risk penalty. |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | All; highest impact: dairy_liquid, legume_system, whole_food_fat (potassium-rich categories) |
| **candidate_signal_name** | `na_k_ratio` |
| **should_affect_score_now** | false — potassium is not required on Israeli nutrition labels; coverage will be <30% |
| **required_input_fields** | `normalized_nutrition_per_100g.sodium_mg`, `normalized_nutrition_per_100g.potassium_mg` |
| **risk_of_misuse** | Potassium is rarely declared on Israeli labels — applying a Na:K ratio adjustment when potassium is absent would default to the worst-case assumption; must handle missing data explicitly |
| **notes** | Implement as a score modifier: when potassium is present and Na:K < 1.0, soften the sodium penalty. When potassium absent, use sodium-only scoring. A missing potassium field should never be treated as zero. |

---

### EV-012 — Saturated-to-Unsaturated Fat Ratio

| Field | Value |
|-------|-------|
| **finding_id** | EV-012 |
| **concept** | The unsaturated-to-saturated fat ratio is a stronger cardiovascular predictor than absolute saturated fat; the Food Compass lipid ratio method should replace absolute sat fat scoring |
| **scientific_rationale_short** | Scoring absolute saturated fat penalises products rich in healthy unsaturated fats if any saturated fat is present. The ratio approach correctly rewards olive-oil-heavy products (high MUFA/PUFA, some SFA) and penalises palm-oil-heavy products. Short-chain and medium-chain SFAs also have distinct metabolic profiles not captured by total SFA. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — current fat dimension uses absolute saturated fat, which systematically mismeasures the lipid quality of whole_food_fat category products (tahini, nut butters, avocado) |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | whole_food_fat, dairy_liquid, dairy_protein; all fat-containing categories |
| **candidate_signal_name** | `unsaturated_to_saturated_ratio` |
| **should_affect_score_now** | true — fat and saturated fat are standard label fields; unsaturated fat is computable as (total fat − saturated fat) |
| **required_input_fields** | `normalized_nutrition_per_100g.fat_g`, `normalized_nutrition_per_100g.fat_saturated_g` |
| **risk_of_misuse** | Does not differentiate MUFA vs PUFA vs specific SFA types — this is an approximation, not a fatty acid profile. Do not claim precision about specific fatty acids. |
| **notes** | Formula: unsaturated_fat = fat_g − fat_saturated_g. Ratio = unsaturated / saturated. A ratio ≥ 2.0 is protective; < 0.5 is high cardiovascular risk. This is computable TODAY from existing BSIP1 fields. |

---

### EV-013 — Hyper-Palatability / Bliss Point

| Field | Value |
|-------|-------|
| **finding_id** | EV-013 |
| **concept** | Industrial formulation of concurrent sugar + salt + fat + flavour enhancers at optimal ratios overrides sensory-specific satiety and drives overconsumption independently of macronutrient targets |
| **scientific_rationale_short** | The "bliss point" is the engineered product of industrial food chemistry: the precise ratio of sugar, salt, fat, and MSG/flavour enhancers that maximises palatability and suppresses sensory-specific satiety. Products hitting this window are associated with overconsumption in controlled settings regardless of macronutrient profile compliance. |
| **evidence_strength** | Strong (palatability mechanism); Medium (quantification) |
| **confidence_level** | High |
| **BSIP2_relevance** | High — a product can score well on macronutrients while being engineered for overconsumption. The bliss point penalty addresses this blind spot. |
| **implementation_complexity** | Medium |
| **recommended_action** | research_further |
| **affected_categories** | snack_bars, cereal_system, sauce_spread (condiments), any highly processed product |
| **candidate_signal_name** | `bliss_point_synergy_score` |
| **should_affect_score_now** | false — mathematical threshold definition is product-dependent; exact quantification requires research calibration |
| **required_input_fields** | `normalized_nutrition_per_100g.sugars_g`, `normalized_nutrition_per_100g.sodium_mg`, `normalized_nutrition_per_100g.fat_g`, `extracted_flavors`, `extracted_additives` |
| **risk_of_misuse** | Applying a bliss point penalty without calibrated thresholds will falsely penalise naturally salt + fat + sugar products (e.g., dates, mixed nuts, cheese) |
| **notes** | Pre-condition: the Siga MUP framework (EV-001) and at-risk additive count (EV-002) must be implemented first. Bliss point scoring should only activate on products that also have MUP > 0 to avoid penalising natural matrices. |

---

### EV-014 — Hard Cheese Matrix Exception (Calcium Saponification)

| Field | Value |
|-------|-------|
| **finding_id** | EV-014 |
| **concept** | Hard cheese matrices promote calcium saponification of saturated fatty acids during intestinal transit, reducing net absorbable lipid by ~15% compared to liquid dairy or emulsions |
| **scientific_rationale_short** | In solid dairy matrices, free calcium ions react with liberated saturated fatty acids in the small intestine to form insoluble calcium soaps that resist lipolytic absorption and are excreted. This attenuates postprandial lipemia in hard cheese relative to butter or liquid milk with equivalent fat content. The calcium-to-saturated fat threshold must be met for the effect to apply. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — standard nutritional profiling overestimates the absorbable fat load of hard cheeses. Governs the cheese matrix exception to the saturated fat penalty. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now (category-specific to hard cheese) |
| **affected_categories** | dairy_protein (hard cheese sub-pool); explicitly NOT soft cheese, cream cheese, or liquid dairy |
| **candidate_signal_name** | `matrix_saponification_index` |
| **should_affect_score_now** | false — requires routing to confirm hard cheese sub-pool AND calcium content (not always on Israeli labels); apply only when both signals are confirmed |
| **required_input_fields** | `archetype`, `canonical_name_he`, `normalized_nutrition_per_100g.fat_saturated_g`, `normalized_nutrition_per_100g.fat_g` |
| **risk_of_misuse** | Must not be applied to processed cheese, cream cheese, labaneh, or dairy spreads — saponification requires a solid matrix. Hard vs processed cheese distinction must come from routing, not this signal alone. |
| **notes** | Misconception 11 in the source explicitly states that the saturated fat in cheese does not carry the same CVD risk as butter. This is the scientific basis for a hard cheese governance exception already partially implemented in Bari. This finding formally registers it with evidence grounding. |

---

### EV-015 — Fermentation Bonus (Phytate Degradation + Structural Changes)

| Field | Value |
|-------|-------|
| **finding_id** | EV-015 |
| **concept** | Fermentation degrades anti-nutritional phytic acid via endogenous phytases, improving mineral bioaccessibility; simultaneously reduces NOVA score and restructures the protein matrix |
| **scientific_rationale_short** | Fermentation activates phytases that dephosphorylate phytic acid, significantly increasing bioaccessibility of Fe²⁺, Zn²⁺, Mg²⁺. Fermented grain products (sourdough, tempeh) also show reduced glycemic response from organic acid production and restructured starch. The effect is time- and strain-dependent but directionally consistent across fermented products vs unfermented equivalents. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — already partially implemented in BSIP2 for bread (sourdough fermentation signal). This finding formally grounds the fermentation bonus and extends it to all fermented categories. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now |
| **affected_categories** | bread, cereal_system, dairy_protein (yogurt/kefir), whole_food_fat (tempeh/miso) |
| **candidate_signal_name** | `fermentation_quality_bonus`, `fermentation_marker_detected` |
| **should_affect_score_now** | true — fermentation markers are already extracted by BSIP1 (`extracted_fermentation_markers`); scoring can use this signal now |
| **required_input_fields** | `extracted_fermentation_markers`, `ingredients_list` |
| **risk_of_misuse** | "Sourdough flavour" (from vinegar or flavour additives) is not the same as genuine long-fermentation sourdough. Detection must check for authentic fermentation markers, not just flavour claims. |
| **notes** | The sourdough D6 threshold problem (identifying genuine sourdough from label data) is documented in governance. This finding does not resolve that problem but justifies the bonus when authentic fermentation is confirmed. |

---

### EV-016 — Fortified vs Intrinsic Nutrient Distinction

| Field | Value |
|-------|-------|
| **finding_id** | EV-016 |
| **concept** | Synthetic fortification vitamins and minerals lack the matrix co-factors and food-bound structures of intrinsic nutrients; a 30% score discount applies to detected synthetic fortification |
| **scientific_rationale_short** | Intrinsic nutrients are bound within the food matrix alongside co-factors and phytochemicals that affect absorption and utilisation. Synthetic fortification of processed foods (added vitamins, mineral salts) can make products appear nutritionally superior to whole foods on simple profiling grids, but bioavailability equivalence is compound-specific and generally lower. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | High — the DISTORTION-004 (fortification inflation) already registered in Bari governance maps to this finding. This provides the evidence basis for a 30% discount on fortification in nutrient scoring. |
| **implementation_complexity** | Medium |
| **recommended_action** | implement_now |
| **affected_categories** | cereal_system (most endemic), dairy_protein, beverage; any category with DISTORTION-004 active |
| **candidate_signal_name** | `fortification_discount_factor`, `synthetic_fortification_detected` |
| **should_affect_score_now** | false — requires ingredient-level detection of synthetic fortification markers (vitamins listed by chemical name, mineral salts) separate from naturally occurring nutrients |
| **required_input_fields** | `ingredients_list`, `extracted_additives` |
| **risk_of_misuse** | Some fortification genuinely compensates for dietary deficiencies (e.g., iodised salt in a low-iodine population) — apply discount to scoring but not to consumer-facing disclosures that explain the distinction |
| **notes** | DISTORTION-004 implementation in BSIP3 is the resolution path. This finding confirms the 30% discount magnitude referenced in the source document. Fortification signals: ויטמין, נציין, מינרל, iron sulfate, zinc gluconate, etc. |

---

### EV-017 — Sweetener-Induced Gut Dysbiosis

| Field | Value |
|-------|-------|
| **finding_id** | EV-017 |
| **concept** | Sucralose and saccharin alter gut microbiota composition in some individuals, producing impaired glucose tolerance independently of caloric or glycemic load |
| **scientific_rationale_short** | Landmark human intervention studies demonstrate sucralose and saccharin can shift microbiome composition in a subset of "responders," inducing measurable impaired glucose tolerance. Steviol glycosides (stevia) and monk fruit (mogroside V) show better safety profiles in available evidence. High inter-individual variability prevents population-level algorithmic penalisation. |
| **evidence_strength** | Moderate to Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Medium — current BSIP2 treats all non-caloric sweeteners as neutral. A tiered risk classification (high-risk: saccharin, sucralose; neutral: stevia, monk fruit, erythritol) is supported by evidence. |
| **implementation_complexity** | Medium |
| **recommended_action** | research_further |
| **affected_categories** | beverage, snack_bars, dairy_protein (diet/zero products) |
| **candidate_signal_name** | `sweetener_microflora_disruption_risk` |
| **should_affect_score_now** | false — high inter-individual variability prevents population-level scoring; implement as a flag/disclosure, not a score deduction |
| **required_input_fields** | `ingredients_list`, `extracted_sweeteners` |
| **risk_of_misuse** | Applying a score penalty for saccharin would unfairly disadvantage long-standing diet products where the risk is population-level, not individual |
| **notes** | Related to EV-004 (allulose) and EV-005 (polyols). The three sweetener findings together form a sweetener tier: (1) allulose/mogroside V — preferred, (2) stevia/erythritol — neutral, (3) sucralose/saccharin — flag. |

---

### EV-018 — Reconstitution-Induced Matrix Destruction

| Field | Value |
|-------|-------|
| **finding_id** | EV-018 |
| **concept** | Reconstituted dried ingredients (milk powder, starch isolates, egg solids) fail to re-establish cellular compartmentalisation; they behave physiologically as liquid matrices with accelerated enzymatic digestion |
| **scientific_rationale_short** | Drying and reconstituting food ingredients disrupts the original cellular architecture. Reconstituted milk powder does not reform the protein-lipid microstructure of fresh milk. This produces accelerated enzymatic digestion similar to liquid forms rather than intact whole foods. |
| **evidence_strength** | Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Medium — products listing "reconstituted" milk or "milk powder" as primary dairy source should receive a matrix quality downgrade relative to fresh dairy equivalents |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now (category-specific to dairy) |
| **affected_categories** | dairy_liquid, dairy_protein |
| **candidate_signal_name** | `reconstituted_matrix_flag` |
| **should_affect_score_now** | true — "reconstituted" and "milk powder" are detectable in ingredient list; flag is simple text match |
| **required_input_fields** | `ingredients_list` |
| **risk_of_misuse** | Some legitimate high-quality products (yogurt made from milk powder in regions with limited fresh supply) would be penalised — apply as a flag with disclosure note rather than a hard score deduction |
| **notes** | Hebrew signals: חלב מחולב, חלב מרוכז, חלב אבקה, מוחזר, reconstituted. Implementation is trivial and should be bundled with the dairy pipeline run. |

---

### EV-019 — Prebiotic Gum and Natural Thickener Classification

| Field | Value |
|-------|-------|
| **finding_id** | EV-019 |
| **concept** | Gum arabic, arabinogalactan, and similar natural polysaccharide gums support Bifidobacterium/Lactobacillus growth and should be classified as prebiotic fibers, not processing additives |
| **scientific_rationale_short** | Unlike synthetic emulsifiers (CMC, P80), gum arabic serves as a fermentable fiber substrate for beneficial gut bacteria. It does not degrade the mucosal lining; it promotes bifidogenic growth and pathogen inhibition. Penalising it as a generic additive conflates it with genuinely harmful surfactants. |
| **evidence_strength** | Moderate |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — the emulsifier penalty framework (EV-003) must explicitly exempt gum arabic and similar prebiotic gums |
| **implementation_complexity** | Low |
| **recommended_action** | implement_now |
| **affected_categories** | All (gum arabic appears across many processed categories) |
| **candidate_signal_name** | `prebiotic_gum_exemption` |
| **should_affect_score_now** | true — simple ingredient text exemption; no calculation required |
| **required_input_fields** | `ingredients_list`, `extracted_additives` |
| **risk_of_misuse** | Excessive doses of gum arabic still cause transient bloating — exemption from emulsifier penalty is correct, but should not confer positive prebiotic credit without quantity data |
| **notes** | Prebiotic gum exemption list: gum arabic (גומי ערבי, E414), arabinogalactan, acacia gum. Xanthan gum and locust bean gum are neutral (not prebiotic, not harmful at label doses) — neither penalise nor credit. |

---

### EV-020 — Resistant Starch Identification

| Field | Value |
|-------|-------|
| **finding_id** | EV-020 |
| **concept** | Resistant starch (RS1–RS4) escapes small intestinal digestion, reduces net glycemic carbohydrate load, and improves insulin economy |
| **scientific_rationale_short** | Resistant starches resist pancreatic amylase, acting as prebiotic substrates in the colon. RS3 (retrograded starch from cooked-cooled starches) and RS4 (chemically modified) are common in commercial products. RS-rich ingredients include green banana flour, raw potato starch, and high-amylose corn starch. These should be subtracted from net glycemic carbohydrate calculations. |
| **evidence_strength** | Moderate to Strong |
| **confidence_level** | High |
| **BSIP2_relevance** | Medium — green banana flour and raw potato starch are increasingly used in clean-label products; incorrectly penalising them as high-carb ingredients produces false low scores |
| **implementation_complexity** | Medium |
| **recommended_action** | research_further |
| **affected_categories** | snack_bars, cereal_system, whole_food_fat (clean-label keto products) |
| **candidate_signal_name** | `resistant_starch_flag`, `net_glycemic_carb_g` |
| **should_affect_score_now** | false — RS3 (retrograded) cannot be confirmed from label; RS-rich ingredient detection is achievable but quantity unknown |
| **required_input_fields** | `ingredients_list` |
| **risk_of_misuse** | RS content of a product changes with cooking history (RS3 increases with cooling) — applying a static RS bonus without process confirmation would be inaccurate |
| **notes** | RS ingredient signals: קמח בננה ירוקה (green banana flour), עמילן תפוח אדמה גולמי (raw potato starch), עמילן תירס עמילוזי גבוה. Implement as a flag + conservative partial credit pending better data. |

---

### EV-021 — Live-Culture Dairy A-Ceiling Governance Ruling

| Field | Value |
|-------|-------|
| **finding_id** | EV-021 |
| **concept** | Plain, additive-free, live-culture dairy (yogurt + white cheese) MAY reach grade A, earned organically by score — in parallel to whole milk at 85/A. B is the truthful ceiling for the sweetened/stabilized mainstream, NOT for the category. |
| **scientific_rationale_short** | A plain live-culture yogurt is a whole-milk matrix PLUS a documented positive (fermentation, EV-015: phytase mineral bioaccessibility, organic-acid glycemic dampening, restructured protein). It carries no snack-bar-style irreducible compromise: sugar is intrinsic lactose, fat is intrinsic dairy fat. It therefore inherits the MILK precedent (clean dairy matrix → A), not the snack-bar B-ceiling precedent. The only sub-milk downgrade is milk-powder standardization (NOVA 3 read), a fortification step, not an engineering compromise. |
| **evidence_strength** | Strong (composes EV-014/015/018/019 + frozen milk precedent) |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — governs whether an A may appear on the yogurt and white-cheese shelves. The run_yogurt_003 "0 grade-A" result is mostly the EV-015 culture-detection gap (0/88 markers matched), not a punitive ceiling; restoring detection lifts the cleanest tier to ~80–86 → A organically (~2–5 earned A's). |
| **implementation_complexity** | Low (no new rule — composes EV-015 mechanism) |
| **recommended_action** | governance_ruling — **Product co-signed 2026-06-01 (TASK-139A CLOSED)**; activation now gated only on EV-015 culture-vocab coverage restoration + A-threshold reconciliation (both inherited by TASK-139B) |
| **affected_categories** | dairy_protein sub-pools: yogurt, white_cheese (explicitly NOT a global rule) |
| **candidate_signal_name** | (no new signal — uses `fermentation_marker_detected` per EV-015) |
| **should_affect_score_now** | false — Product co-sign ✅ (2026-06-01); A-condition C1–C6 still cannot activate until (a) EV-015 Israeli culture-vocabulary coverage is restored (currently 0%, precondition for C3) and (b) the A-threshold (80 vs 85) is reconciled — both inherited by TASK-139B |
| **required_input_fields** | `extracted_fermentation_markers`, `added_sugar_sources_count`, `extracted_additives`, `nova_level`, `archetype`, `confidence_level` |
| **risk_of_misuse** | (1) Reading EV-014 hard-cheese saponification as a back-door A for processed/spreadable cheese — it is a fat-absorption exception, not an A-grant. (2) Crediting "sourdough/culture flavour" without microbial strain markers. (3) The `סוכרים`→`סוכר` nutrition-text false positive inflating `added_sugar_sources_count` and wrongly failing C1 on plain yogurts. (4) Restoring the manual shelf's blanket 5×A-by-format instead of earned A's. |
| **notes** | Source: TASK-139A ruling `02_products/yogurt_system/reports/dairy_a_ceiling_ruling_139A.md`. A-eligibility condition (RULING-DAIRY-A-01): ALL of C1 no added sugar · C2 no engineered additives · C3 live culture confirmed AND credited · C4 intact dairy matrix (reconstituted base NOT eligible, EV-018) · C5 correct dairy routing · C6 verified confidence. Gates TASK-139B/139C, TASK-142, TASK-143. Published-grade consequence: yogurt A-count 5→~2–5 (earned), median 72→~61–63 — flagged for Product co-sign. |

#### EV-021 AMENDMENT A1 (2026-06-02, TASK-169 / TASK-169B) — blanket cheese A-cap → conditional A-eligibility gate

| Field | Value |
|-------|-------|
| **supersedes** | The **cheese** implementation of RULING-DAIRY-A-01, which had collapsed C1–C6 into a blanket `a_eligible_pre_routing = False` for ALL `dairy_protein` cheese products (withholding every grade-A cheese regardless of merit). This amendment retires the blanket cap for cheese and replaces it with a conditional gate. The yogurt C1–C6 conditions above remain as written for the yogurt category. Audit trail preserved: the original blanket-cap rationale (run_003 cottage NOVA-3 regression + supplement-protein compression made a raw A untrustworthy) is documented in the EV-021 lineage above; the recalibration (R1–R7, EV-027/030–033) that fixed those root causes is what makes a conditional gate safe now. |
| **owner_ruling** | Binding, 2026-06-02 (TASK-169 / TASK-169B). The blanket no-A cap existed to stop a high score driven by protein/processing alone — on a composite that does NOT score sodium or saturated fat into the cheese grade — from showing a misleadingly clean grade A. With R1 (category-relative protein), R5 (graded sat-fat penalty) and R7 v1.1 (gated culture bonus) in place, the blanket cap is now over-broad. Replace it with a **conditional A-eligibility gate**: a cheese may display grade A only if it is genuinely clean on the two axes the composite under-weights for cheese — **sodium AND saturated fat**. A high score on a salty or fatty cheese is still display-capped to B. |
| **predicate** | `a_eligible = (score earns A-band) AND (sodium_mg ≤ 400) AND (sat_fat_g is not None AND sat_fat_g ≤ 4.0)`. Units: sodium mg/100g, saturated fat g/100g. A product that earns an A-band score but fails either axis is **display-capped to B** (not withheld from display). |
| **threshold_grounding** | Israeli MoH red-label lines (`RED_LABEL_THRESHOLDS`, constants.py): sodium 600 mg/100g, sat-fat 5.0 g/100g. Per the "best ≠ excellent" doctrine, "clean" must sit **meaningfully below** the red line, not at it. **Sodium ≤ 400 mg = 67% of the red line** and equals the run_cheese_004 shelf Q3 (sodium: min 30 / Q1 291 / median 350 / Q3 400 / max 720; the 7905 reading is an OCR outlier, excluded n=58). **Sat-fat ≤ 4.0 g = 80% of the red line**, sitting between shelf Q1 (3.0) and median (5.4); it admits the genuinely-lean fresh-cheese cluster (≤5% milkfat cottage/white cheese, sat-fat 0.6–3.25) and excludes both the 30/57 of the shelf already over the 5.0 red line and the 9%-milkfat tier at sat-fat 5.4. |
| **missing_data_rule** | **Missing sat-fat BLOCKS A (fail-closed).** A cheese with `sat_fat_g = None` cannot satisfy "genuinely clean on saturated fat" — the gate cannot be evaluated, and the gate exists precisely because the composite does not see this axis. Conservative default → cap to B. Same fail-closed logic for null sodium. (In run_cheese_004 only 2/59 lack sat-fat; neither is an A candidate.) Note: this is fail-toward-caution, consistent with R4's missing-data → stricter-NOVA-3 convention. |
| **verdict_on_13_staged_A** | Applied to the 13 staged grade-A cheeses in `cheese_frontend_v2.json` (run_cheese_004, BARI_RECAL_P0=on): **11 PASS → stay A; 2 CAP → B.** Cottage 1% PASSES (Na 350, sat-fat 0.6). The 2 caps are both the 9%-milkfat cottage tier — `che-4127336 קוטג' 9% שומן` and `che-41452 קוטג' מהדרין 9% שומן` (both 81/A, sat-fat **5.4 g > 4.0**, over the Israeli red line) → correctly display-capped to B. No A is capped on sodium (max A-candidate sodium = 350). |
| **affected_categories** | `dairy_protein` (cheese) ONLY. Cheese-scoped per owner instruction; does NOT touch yogurt, milk, hummus, or any other category's A-eligibility. The yogurt C1–C6 conditions are unchanged. |
| **gated_by** | `BARI_RECAL_P0` (same flag as the recalibration). Flag OFF → original behavior; flag ON → conditional gate. |
| **evidence_strength** | Moderate (thresholds are a calibrated judgement anchored to the real shelf distribution + the regulatory red line; the exact cut points 400/4.0 are values calls flagged for owner). |
| **status** | Owner-approved (TASK-169) for cheese scope; Product Agent D7 co-sign required before live repoint, consistent with the existing recal governance. |

---

### EV-022 — Israeli Live-Culture Label Vocabulary (Extraction Coverage Restored)

| Field | Value |
|-------|-------|
| **finding_id** | EV-022 |
| **concept** | The BSIP1 enricher missed the way real Israeli labels write the live-culture positive, so EV-015's input was empty for the yogurt category (run_yogurt_003: 0/88 markers). Extending `FERMENTATION_TERMS` to the observed label vocabulary restores detection. Non-interpretive term matching only — no new scoring rule. |
| **scientific_rationale_short** | EV-015 (fermentation bonus) reads `extracted_fermentation_markers`, but `FERMENTATION_TERMS` matched only `תרבויות`/`ביפידובקטריום`/`לקטובציל`. Shufersal labels declare cultures as `חיידק פרוביוטי` / `חיידקי ביפידוס` / `BIFIDUS` / `חיידקי Bio` / `חיידקי יוגורט` / `תרבית`, so the category-defining positive was invisible to scoring. Detection 0/88 → **49/88 has_live_cultures**, 51/88 any fermentation marker. |
| **evidence_strength** | Strong (direct label observation; run_yogurt_003 Shufersal corpus, 88 SKUs) |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — supplies the EV-015 input and satisfies EV-021 RULING-DAIRY-A-01 **condition C3** (live culture confirmed AND credited), previously blocked at 0% coverage. |
| **implementation_complexity** | Low (term-list extension only) |
| **recommended_action** | implemented (TASK-139B) |
| **affected_categories** | yogurt, dairy_protein, white_cheese |
| **candidate_signal_name** | (no new signal — uses `fermentation_marker_detected` per EV-015) |
| **should_affect_score_now** | false — extraction/observability fix, not a scoring rule. EV-015 bonus is already active, but no category is re-scored or published here; yogurt grade publication stays gated on TASK-139C (A-threshold) and the live DEC-005 manual shelf is untouched. |
| **required_input_fields** | `ingredients_text_he` |
| **label_observability** | Signal: live-culture declaration. Coverage **before 0/88 (0%) → after 49/88 (56%)** has_live_cultures. Collision audit: **0 new markers** on any frozen/non-dairy corpus (snacks run_001, bread_light_001, bread_retail_001/003, cereals_001, hummus_001, milk_001/002); the one bread match (`לחם הרים`, `מחמצת פרוביוטית`) credits only the pre-existing `מחמצת` term — unchanged. |
| **guards_verified** | Golden corpus regression **11 PASS / 1 WARN / 0 FAIL** (WARN = pre-existing `anchor_soy_drink` acceptable-secondary, change-independent — regression reads stored traces + `structural_classifier.py`, never the enricher). Enricher unit tests **64/64 PASS**. Frozen invariants (milk 85/A, bread retail_003, snk-001 70/B) **unmoved** — 0 new markers in their corpora, no re-score. |
| **rollback** | `git revert` of the `FERMENTATION_TERMS` block in `03_operations/bsip1/core/ingredient_enricher.py` (+ the `run_yogurt_003` entry in `enrich_runner.py`) restores prior 0/88 behavior; run_yogurt_003 BSIP1 output is non-authoritative and re-enrichment is idempotent. Notify: Data Architecture + Nutrition (EV-015/EV-021 owner). |
| **notes** | Source: TASK-139B (`ingredient_enricher.py` FERMENTATION_TERMS extension; re-run via `enrich_runner.py --run run_yogurt_003`). Implements the EV-021 C3 / Gap-2 culture-vocabulary fix. Residual: `חיידקי L.casei DN114-001` (1 DanActive-style SKU) unmatched — Latin strain code outside task-named vocab; known minor gap. Recorded 2026-06-01. |

---

### EV-023 — Grade-Boundary Reconciliation (A-Threshold 80 vs 85)

| Field | Value |
|-------|-------|
| **finding_id** | EV-023 |
| **concept** | The canonical `.claude/scoring.md` Grades table carried a stale 5-grade scale (A=85–100, no S-grade, every band shifted) that disagreed with the live engine `constants.py GRADE_THRESHOLDS` (6-grade: S≥90, A≥80, B≥65, C≥50, D≥35, E) and with the frozen milk run_004 artifact (A≥80; whole milk 85=A). Corrected the doc to the engine scale; **A≥80 ratified** as the dairy A cutoff. No engine/score change. |
| **scientific_rationale_short** | The A-threshold ambiguity (80 vs 85) flagged in RULING-DAIRY-A-01 / EV-021 decided whether the cleanest plain/bio/lactose-free dairy (~80–86) reaches grade A. The live engine and the frozen milk run already compute A≥80 (six-grade S/A/B/C/D/E); only the scoring.md table was stale. Adopting A≥80 lets clean live-culture dairy reach A organically — the identical earned mechanism as whole milk at 85/A — satisfying EV-021 A-reachability with no category A-grant. |
| **evidence_strength** | Strong (direct: `constants.py GRADE_THRESHOLDS` + `batch_run_milk_004` header both A≥80; frozen whole milk 85=A) |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — resolves the last RULING-DAIRY-A-01/EV-021 precondition (A-threshold) blocking yogurt/cheese grade publication (TASK-139 parent; TASK-142/143). |
| **implementation_complexity** | Trivial (documentation correction only; engine unchanged) |
| **recommended_action** | implemented (TASK-139D) — Product co-signed 2026-06-01 |
| **affected_categories** | yogurt, dairy_protein, white_cheese, cheese_spreads, ALL (grade-doc correctness) |
| **candidate_signal_name** | (no new signal — grade boundary already in `constants.py GRADE_THRESHOLDS`) |
| **should_affect_score_now** | false — no engine change. `constants.py` already = S≥90/A≥80/B≥65/C≥50/D≥35/E; this only corrects the stale `scoring.md` table to match. No category is re-scored or published by this entry; yogurt/cheese grade publication proceeds under the TASK-139 parent re-score with A≥80 confirmed. |
| **required_input_fields** | `final_score` (→ `score_to_grade()`) |
| **label_observability** | Not a label signal — a grade-band boundary. Authoritative source = `constants.py GRADE_THRESHOLDS`. After fix, `scoring.md` matches the engine across all bands: **S 90–100 / A 80–89 / B 65–79 / C 50–64 / D 35–49 / E 0–34**. |
| **guards_verified** | No code/scoring change → golden regression unaffected (reads `constants.py`, unchanged). Frozen invariants unmoved: whole milk 85→A (A≥80), snk-001 70→B (B≥65), bread retail_003 grades all identical before/after — the engine already used A≥80; only the doc was wrong. The hummus batch-report string "A 85–100" is a separate stale display artifact (cosmetic, non-authoritative), flagged for optional cleanup. |
| **rollback** | `git revert` of the `scoring.md` grade-table edit restores the prior (stale) 5-grade table. No engine/score artifact touched; reversible with zero score impact. |
| **source** | TASK-139D (A-threshold reconciliation, folded out of closed TASK-139C). Basis: `dairy_a_ceiling_ruling_139A.md` §A-threshold; `constants.py GRADE_THRESHOLDS`; `batch_run_milk_004` frozen header. |
| **date_recorded** | 2026-06-01 |
| **notes** | Resolves the "80 vs 85" item RULING-DAIRY-A-01/EV-021 said "must be reconciled before grades publish." Outcome: A≥80 (six-grade scale) is authoritative; `scoring.md` corrected. Product co-signed ("Confirmed", 2026-06-01). Unblocks the TASK-139 parent closing re-score → TASK-142/143. |

### EV-024 — Culture-Credit Propagation Fix (BSIP1 → BSIP2 Scorer)

| Field | Value |
|-------|-------|
| **finding_id** | EV-024 |
| **concept** | TASK-139B extended the **BSIP1 enricher** `FERMENTATION_TERMS` to real Shufersal live-culture label vocabulary, but the **BSIP2 scorer** derives `has_fermentation` from an INDEPENDENT list (`signal_extractor.FERMENTATION_MARKERS_HE`) and never reads the BSIP1 flag. run_yogurt_003 therefore **detected 49/86 live-culture SKUs in BSIP1 yet credited 0/86 in the score** (`fermentation_bonus_applied`=0; distribution byte-identical to pre-139B). The parent closing re-score surfaced this. **Fix:** mirrored 139B vocabulary into `FERMENTATION_MARKERS_HE` so the already-active fermentation bonus (R-02 direct + WFI `ferm_bonus` +5) sees real labels. Non-interpretive substring matching only — no new rule/weight/threshold/cap. |
| **scientific_rationale_short** | RULING-DAIRY-A-01 **C3** requires live culture *confirmed AND credited*. Detection without crediting leaves C3 structurally unsatisfiable. The mirror makes the existing fermentation positive earn its already-defined bonus on genuine live-culture dairy. |
| **evidence_strength** | Strong (direct: BSIP1 `has_live_cultures` 49/86 vs BSIP2 `has_fermentation` 3/86 pre-fix → 34/86 post-fix; bonus firing per WFI dimension notes). |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — the TASK-139 parent closing re-score of run_yogurt_003; gates TASK-142/143. |
| **implementation_complexity** | Trivial (term-list extension mirroring approved sibling EV-022). |
| **recommended_action** | implemented (TASK-139 parent). Nutrition truthfulness sign-off done; **Product co-sign required** for the published-candidate movement (12 SKUs C→B). |
| **affected_categories** | yogurt, dairy_protein, white_cheese, cheese_spreads, maadanim (live dairy, future re-score) |
| **candidate_signal_name** | `has_fermentation` (existing) — vocabulary coverage extended, not a new signal |
| **should_affect_score_now** | true — cultures are a label-observable, score-bearing positive already wired to R-02 / WFI. The fix repairs vocabulary coverage only; it manufactures **no grade A** (0 A before and after) — no category grant. |
| **required_input_fields** | `ingredients_text` (live-culture declaration) |
| **label_observability** | Fully label-observable. Added to the BSIP2 scorer: תרבויות, חיידק פרוביוטי (+construct/plural), חיידקי ביפידוס/יוגורט/אצידופילוס, ביפידוס/bifidus, תרבית. Mirrors EV-022. |
| **guards_verified** | (1) **Collision audit** — 0 `has_fermentation` flips on every frozen/non-dairy corpus (milk_001/002, snacks run_001, bread_light_001, bread_retail_003 [262-file scan], cereals_001/002, hummus_001). (2) **Frozen isolation** (OLD-vs-NEW marker toggle, in-memory full-pipeline recompute): milk_004 top **85.0/A** unchanged, snacks top **70.0/B (snk-001)** unchanged, **0 SKUs moved by this patch**. (3) Golden structural regression **11 PASS / 1 WARN** (pre-existing `anchor_soy_drink`, change-independent) **/ 0 FAIL**. (4) Router regression **12/12 PASS**. |
| **rollback** | Working-tree edit (uncommitted). Rollback = restore the `FERMENTATION_MARKERS_HE` block in `signal_extractor.py` → reverts `has_fermentation` to 3/86 and distribution to B17/C44/D24/E1. run_yogurt_003 BSIP2 output is NON-AUTHORITATIVE; re-score is idempotent. Notify: Data Architecture + Nutrition + Product. |
| **source** | TASK-139 parent closing re-score. Files: `signal_extractor.py` `FERMENTATION_MARKERS_HE`; `batch_run_yogurt_003.py`; `run_yogurt_003_run_summary.json`. |
| **date_recorded** | 2026-06-01 |
| **notes** | **Re-score delta (86 SKUs):** B 17→29, C 44→32, D 24 (=), E 1 (=); **A 0→0 (unchanged)**; median 55.7→56.1; ceiling 78.2→78.7/B. 12 live-culture SKUs C→B. **Truthful 0-A finding (Nutrition sign-off):** no SKU satisfies C1–C6 in this corpus — NOVA dist 0×N1 / 4×N2 / 36×N3 / 48×N4; the 4 clean NOVA-2 plain/goat yogurts have **empty ingredient panels** (C3 impossible) and are dimensionally capped 65–72/B by low `nutrient_density` (10–26)/`protein_quality`, not by any cap; all higher scorers are NOVA-3/4 engineered/sweetened (fail C1/C2). **B/78.7 is the truthful ceiling for run_yogurt_003.** Upholds 139A qualitative ruling (B truthful for mainstream; A reachable in principle, earned only) but **contradicts its quantitative ~2–5 earned-A estimate.** Open (non-blocking, Nutrition): goat-milk 85/A vs goat-yogurt 66.7/B gap — is yogurt `nutrient_density` scored too harshly vs the milk table? Residual: BSIP1 49 vs BSIP2 34 `has_fermentation` — ~15 SKUs use culture vocab still unmirrored (all NOVA-3/4 sweetened → cannot reach A). Registry: TASK-139B was CLOSED on BSIP1-only detection; its score-crediting DoD was completed here — Central Controller to decide bookkeeping (reopen 139B vs note in parent). |

```yaml
study_objects:
  - claim: "Fermentation of dairy produces beneficial structural changes including protein pre-digestion, lactose reduction, and SCFA production by live cultures"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: A
    source_doi: "10.3390/nu11081781"
    notes: "Systematic review of fermented dairy and gut health outcomes. Population: healthy adults. Dose: standard yogurt/fermented dairy serving. This is mechanism-level evidence supporting the existing fermentation bonus in BSIP2's WFI dimension. EV-024 itself is a vocabulary/detection fix, not a new scientific claim — this study object grounds the underlying scientific rationale for the bonus that the fix enables to fire correctly."
  - claim: "Live bacterial cultures (lactobacilli, bifidobacteria) in yogurt are detectable and viable at point of consumption"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: B
    source_doi: "internal:bsip2_evidence_registry_v1.md"
    notes: "Label-observability claim — not a mechanistic RCT. The 'study' here is the BSIP1/BSIP2 corpus analysis: 49/86 Shufersal yogurt SKUs declared live cultures on their Hebrew ingredient panels (RULING-DAIRY-A-01 C3). Tier B reflects that label declaration is a reliable (though not perfect) proxy for culture presence, supported by regulatory requirements for yogurt labeling in Israel."
```

### EV-025 — Cream-Cheese / Spread Router Anchor (Identity, not Score)

| Field | Value |
|-------|-------|
| **finding_id** | EV-025 |
| **concept** | `router_v2.py` had a cottage hard anchor (`קוטג'→dairy_protein`) and Stage-2 dairy signals carried plain white cheese / labaneh, but **no anchor for the cream-cheese/spread pool**. TASK-142 run_cheese_001 showed **all 26 cream-cheese SKUs misrouting** (גבינת שמנת/ממרח גבינה/פילדלפיה/נפוליאון → default/whole_food_fat); total misroute **47.4% >> 5% gate**, and the 3 `default` SKUs went insufficient. Fix: add four specific cream-cheese hard anchors → dairy_protein, with a `נפוליאון` cake-exclusion. **Identity/routing change only — no scoring weight/threshold/penalty/cap touched.** |
| **scientific_rationale_short** | Cream cheese is high-fat / low-protein / often flavored, so it lacks the dairy *signal* strength that carries plain white cheese into dairy_protein; without a name anchor it falls to `default` (no signal) or `whole_food_fat` (fat-led). The anchor restores correct dairy identity so the dairy calorie table + `is_plain_dairy` (R-04) cap relief apply, and the dairy A-ceiling (EV-021) governs it. Same class as the cereal-anchor (QA-CER-001) and yogurt-anchor (TASK-139C) gaps. |
| **evidence_strength** | Strong (direct: run_cheese_001 misroute 47.4% [27/57; 26 cream] → run_cheese_002 misroute 1.8% [1/57]; insufficient 3→0). |
| **confidence_level** | High |
| **BSIP2_relevance** | Direct — unblocks the TASK-142 cheese-spreads misroute<5% / insufficient-0% DoD (run_cheese_002). |
| **implementation_complexity** | Trivial (4 hard anchors + 1 exclusion list; no scoring logic). |
| **recommended_action** | implemented (TASK-145). Routing-only; Nutrition/Product sign-off pending only for the cheese grade *publication* (separate from this routing fix). |
| **affected_categories** | cheese_spreads (dairy_protein routing). Collision-audited against maadanim / yogurt_system / milk corpora — 0 name matches; frozen categories unaffected. |
| **candidate_signal_name** | (no new signal — hard anchor terms in `router_v2.HARD_ANCHORS`) |
| **should_affect_score_now** | false (routing/identity) — it changes *which category table* a product is scored under, but adds no scoring rule. Cream cheese moving from default/whole_food_fat to dairy_protein corrects its identity; the dairy A-ceiling still gates any A. |
| **required_input_fields** | `canonical_name_he` (100% Hebrew coverage on the cheese corpus). |
| **label_observability** | Fully observable — substring match on the product name. Anchors: `גבינת שמנת` (cream_cheese), `ממרח גבינה` (cheese_spread), `פילדלפיה` (cream_cheese), `נפוליאון` (cream_cheese, with cake exclusion [עוגה/עוגת/פס/מאפה/בצק]). Bare `שמנת` deliberately NOT added (sour/sweet/whipping cream are not cheese). |
| **guards_verified** | (1) Router regression **15/15 PASS** (12 frozen + 3 new cream-cheese entries incl. napoleon-cake exclusion). (2) Spot-check: גבינת שמנת/ממרח גבינה/פילדלפיה/נפוליאון-cheese → dairy_protein; עוגת פס נפוליאון, שמנת חמוצה, שמנת מתוקה → default (correctly NOT dairy). (3) Collision audit: 0 name matches in maadanim/yogurt/milk corpora → no frozen-category routing movement. (4) Engine otherwise unmodified; determinism confirmed (run_cheese_001 re-run on patched router == run_cheese_002). |
| **rollback** | `git revert` of the cream-cheese HARD_ANCHORS hunk + `נפוליאון` ANCHOR_EXCLUSIONS entry in `router_v2.py` (and the 3 regression-corpus entries) restores prior behavior (cheese misroute 47.4%). No score artifact promoted (run_cheese_001/002 NON-AUTHORITATIVE). Notify: Data Architecture + Scoring Governance Lead. |
| **source** | TASK-145 (spun off TASK-142 QA-CHS-001). Files: `router_v2.py` HARD_ANCHORS + ANCHOR_EXCLUSIONS; `router_regression_corpus.json` (+3 entries); `batch_run_cheese_002.py`; `run_cheese_002_run_summary.json`. |
| **date_recorded** | 2026-06-01 |
| **notes** | **run_cheese_002 (post-fix):** misroute 1.8% (only 1 residual — גבינת עזים 32% → snack_bar_granola), insufficient 0/57, grades B23/A6/C27/D1, median 65.0. Cream pool now scores under dairy_protein (median 60.7, C-heavy — high fat + stabilizers). **A-ceiling working:** 6 white-cheese macro-A's (85) all `a_eligible_pre_routing=False` (fail C3 — no confirmed live culture) → WITHHELD; consistent with the conservative dairy ceiling (EV-021). NON-AUTHORITATIVE pending Nutrition/Product grade-publication sign-off. |

### EV-026 — Ingredient-List OCR/Disclaimer-Bleed Sanitization (Upstream Data Hygiene)

| Field | Value |
|-------|-------|
| **finding_id** | EV-026 |
| **task** | TASK-144 (Fix 1) |
| **recorded** | 2026-06-01 |
| **business_signal** | Israeli retailer scrapes routinely glue nutrition-panel text (`ערכים תזונתיים`, `… גרם חלבונים`, `… קל אנרגיה`, `מג נתרן/סידן`) and site disclaimers (`אין להסתמך`, `יש לקרוא…`, `יתכנו טעויות`, `להמחשה בלבד`) onto `ingredients_list`. These phantom "ingredients" inflate `ingredient_count`; with 0 additives and 0 added sugars the **only** thing tripping `nova_proxy.py` `ing_count > 5` → NOVA 3 is this noise (יופלה GO: 8 listed, 3 real). |
| **data_source** | BSIP1 run_maadanim_001 source records; trace `bsip1_maadanim_7290110321031` (raw_count 8 → clean 3). Verified across maadanim corpus + 7-category blast radius. |
| **mechanism** | `signal_extractor.sanitize_ingredient_list()` drops items that are unambiguous bleed (disclaimer/nutrition phrase, ≥2 quantity fragments, digit-led, or panel-connector lead `מתוכם/מהם/הנתונים`) and truncates bleed glued onto a real head at `.n`/digit-quantity/panel-phrase boundaries (bare `.` treated as a separator, NOT a cut — protects multi-ingredient items like `חלב.מייצב`). `nova_proxy` consumes the sanitized count. |
| **layer** | Data hygiene — NOT a scoring rule. No cap/floor/weight/threshold added (no Tension-5 rule-budget cost). |
| **label_observability** | Observable: L1 emits `ingredient_count_raw` + `ingredient_sanitization{raw_count,clean_count,dropped,truncated}` on every trace. |
| **activation_scope** | TASK-144 activation toggle (maadanim run opt-in via `BARI_TASK144_FIXES=on`). Architecturally cross-category-safe, but scoped to maadanim for this deployment. |
| **effect** | GO NOVA 3→2; processing_quality 65→85, WFI 60→85. No real ingredient lost (verified: hummus `חומוס …bleed` salvages `חומוס`; goat-yogurt `.מייצב` separator preserved). |
| **rollback** | `BARI_TASK144_FIXES` unset → sanitizer bypassed, raw counts return. Deterministic, reversible. |

### EV-027 — Fiber "Absent ≠ Zero" for Naturally Fiber-Free Dairy (nutrient_density)

| Field | Value |
|-------|-------|
| **finding_id** | EV-027 |
| **task** | TASK-144 (Fix 2) — HIGHEST-RISK item |
| **recorded** | 2026-06-01 |
| **business_signal** | `nutrient_density` blends protein (65%) and fiber (35%); a MISSING fiber value is read as 0 and drags the dimension down even though the food category is **not expected** to contain fiber. Penalizing a dairy matrix for absent fiber mis-models structural non-applicability as a deficiency (parallel to the whole-food-fat-floor principle: do not penalize a food for not being something it isn't). GO: nd 32.5 → 50.0. |
| **data_source** | maadanim corpus; cross-category blast radius (cereals 0 / bread_light 0 changes confirms gate tightness). |
| **mechanism** | When category ∈ `FIBER_NOT_APPLICABLE_CATEGORIES` AND fiber is genuinely absent/≤0, re-normalize 65/35 → 100/0 (protein-only). |
| **activation_scope** | **TIGHT ALLOWLIST** `("dessert","dairy_protein","yogurt")` — bread, cereal, bars, crackers, crispbread, sauces, whole-food fats, beverages DELIBERATELY EXCLUDED (missing fiber there IS a real deficiency). Plus TASK-144 maadanim-run toggle. |
| **label_observability** | Observable: dimension note records `fiber not-applicable for category '…' (EV-027: protein-only, 65/35→100/0)`. |
| **rollback** | `BARI_TASK144_FIXES` unset → flat 65/35 blend with fiber-as-0 returns. Or empty the allowlist. |
| **risk_note** | Blast radius confirmed this is the rule that can lift clean intact fermented dairy (yogurt/cheese) toward/into A under the milk 85/A precedent (RULING-DAIRY-A-01). Therefore scoped OFF for frozen categories — cross-category adoption requires Product Agent sign-off. |

### EV-028 — Dairy Protein Source Typing (protein_quality)

| Field | Value |
|-------|-------|
| **finding_id** | EV-028 |
| **task** | TASK-144 (Fix 3) |
| **recorded** | 2026-06-01 |
| **business_signal** | The enricher types any product with an isolate marker (incl. `אבקת חלב` milk powder) as `mixed` → ×0.85 protein-quality haircut. Pure-dairy protein (whey + casein + milk protein) is a complete, high-DIAAS protein; the "mixed" haircut (for genuinely blended/uncertain sources) is unjustified. GO: protein_quality 42.5 → 50.0. |
| **data_source** | maadanim corpus; trace `bsip1_maadanim_7290110321031` (source mixed→dairy). |
| **mechanism** | New source class `dairy` (factor 1.0) assigned only when `product_type_dairy` AND every isolate marker is a WHOLE dried-dairy ingredient (milk powder / milk protein / casein) — NOT an extracted protein FRACTION. |
| **collision_check** | **No collision with F2 / TASK-133B** (PROTEIN_QUALITY_MATRIX_DISCOUNT). F2 gates on `protein_matrix_form == "reconstructed"` (RECONSTRUCTED_PROTEIN_MARKERS, which explicitly EXCLUDE milk powder) AND bar categories; EV-028 gates on whole dried-dairy + dairy matrix. The two are mutually exclusive by construction (verified: GO `protein_matrix_form=None`). Fix 3 sets the source FACTOR; F2 sets an independent matrix-form DISCOUNT multiplier. |
| **activation_scope** | TASK-144 maadanim-run toggle. |
| **label_observability** | Observable: protein dimension note records `source=dairy(×1.0)`; L3 `protein_source` / `protein_source_basis`. |
| **rollback** | `BARI_TASK144_FIXES` unset → reverts to `mixed` ×0.85. Or remove `"dairy"` from `source_factors`. |

### TASK-144 companion — Macro-Plausibility Data-Integrity Guard

| Field | Value |
|-------|-------|
| **task** | TASK-144 (companion to EV-026) |
| **business_signal** | OCR parse errors produce impossible macros (e.g. `protein_g=190/100g`, a `19.0`→`190` misread). These survived into the score and — once EV-027/028 lifted the dimensions — produced a spurious 88.7/A (`יוגורט גו נטול לקטוז`). |
| **mechanism** | New consistency check `macros_plausible` (sibling of `kcal_plausible`): False if any macro > 100 g/100g or macro-implied energy > 2× declared kcal + 50. When False → −40 confidence (product flagged `insufficient_data`, no grade). |
| **activation_scope** | Gated to TASK-144 toggle so frozen outputs stay byte-identical; flag itself always computed (observable). Flags exactly 1 product across all frozen corpora (the same 190g artifact) — a correct universal catch deferred to per-category rescore. |
| **rollback** | `BARI_TASK144_FIXES` unset → deduction off. |

### EV-029 — BSIP0 nutritionList Total-Fat Overwrite (Upstream Data Integrity; EV-026 family)

| Field | Value |
|-------|-------|
| **finding_id** | EV-029 |
| **task** | TASK-142A |
| **recorded** | 2026-06-02 |
| **layer** | Data ingestion — NOT a scoring rule. No cap/floor/weight/threshold added (no Tension-5 rule-budget cost). Sibling to EV-026 (both are Shufersal scrape-hygiene defects). |
| **business_signal** | The shared Shufersal `div.nutritionList` parser used `NUTR_LABEL_MAP` with substring matching + break-on-first, mapping BOTH `שומנים` (total fat) and `שומן` (a substring of every "of which" sub-row: `שומן טראנס`, `חומצות שומן רוויות`) to `fat`. The panel lists total fat first, then indented sub-rows; each sub-row label contains `שומן`, re-matched `שומן→fat`, and OVERWROTE total fat. The last fat-bearing row (trans, `פחות מ 0.5`) won → `fat_g` collapsed to 0.5. Saturated fat was NEVER captured (generic `שומן→fat` preceded the specific `שומן רווי→saturated_fat` in iteration order; loop broke first). The Hebrew final-letter trap (`שומן` final-ן is not a substring of `שומנים` regular-נ) is why the legacy map needed both forms — and why a naive stem fix fails. |
| **data_source** | cheese run_cheese_001 raw (62/116 `fat_raw="פחות מ 0.5"`); cereals run_cereals_002 (75/113); yogurt run_yogurt_003 (47/97); maadanim live (88/200); hummus (TASK-039 audit: 59/69). Saturated fat 0% captured in EVERY nutritionList corpus — the universal signature. Live re-scrape verification (2026-06-02): גבינת עזים 32% 0.5→32 (sat 22), קוטג' 9% 0.5→9 (sat 5.4), שמנת לבישול 15% 0.5→15 (sat 9), גבינת שמנת 18% 0.5→22 (sat 14.3). |
| **mechanism** | New shared parser `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`: `classify_nutr_label()` normalizes Hebrew final-forms, classifies most-specific-first (trans→saturated→…→generic fat LAST), and never lets an `מתוכו/מהם` "of which" sub-row map to total fat; `parse_nutrition_list()` keeps first-per-field (totals precede sub-rows). All 5 Shufersal nutritionList scrapers (cheese/cereals/yogurt/maadanim/hummus) now import it — single source of truth (the TASK-039 audit found this in hummus but never centralized the fix, so it re-propagated to 4 more categories). |
| **propagation** | Confirmed into scored traces: yogurt_003 45/88 `fat_g==0.5`, 88/88 saturated absent, **100% `fat_quality` neutralized to 50** ("sat_fat absent → neutral 50"); cereals_002 71/92 `fat_g==0.5`, 92/92 neutralized; maadanim live 88/200 / 200/200; hummus live max fat 5.9g (tahini products should be 15-25g). Effect on final grade is bounded (`fat_quality` weight 0.08) but the dimension is uniformly dead → real fat-quality signal suppressed across these runs; fat also feeds `fat_pct_of_kcal` and `hp_fat_*` patterns. |
| **frozen/live status** | NOT affected (different/earlier path): **milk** (frozen run_004_recalibrated) — Playwright separate-tab capture; **bread** (frozen real_bread_retail_003_v1) — proto_v0 `scrape_bread_retail.py`, no nutritionList, no saturated_fat field; **snacks** — separate path; **yohananof** milk/hummus — `ערכים תזונתיים` textblock regex. Affected & NON-AUTHORITATIVE (NO-GO already): cheese_001/002, cereals_002, yogurt_003. Affected & LIVE: **maadanim** (rescored TASK-136) and **hummus** — require re-scrape + re-score as separate tasks. |
| **TASK-143 verdict** | **run_yogurt_003 is AFFECTED, NOT clean** — `fat_g` collapsed on 45/88 and `fat_quality` neutralized on all 88. The yogurt LIVE swap must wait for a clean re-scrape (run_yogurt_004) + re-score. TASK-143 stays BLOCKED on this. |
| **label_observability** | Observable: QA check `COV-006` (run_qa.py) emits per-product implausibility reasons + corpus %; scraper `main()` composition gate prints a Plausibility line and FAILs ≥5% implausible. `nutrition_implausible()` / `composition_nutrition_report()` are the shared guard. |
| **qa_guard** | `COV-006 Nutrition plausibility` — hard-fails a run when ≥5% of products show the fat-overwrite signature (`saturated_fat > fat`, or `fat≤0.5` with declared energy ≥50 kcal above macro-implied energy). Legitimately low-fat high-carb foods (cereal flakes) pass — their carbs carry the energy. Verified: old broken cheese corpus 31.9% → FAIL; corrected sample → PASS. |
| **activation_scope** | Always-on data-ingestion fix (parser correctness is not toggled). Does NOT alter any frozen/published score by itself — scores only change on the owning category's next re-scrape + re-score. |
| **rollback** | Revert the 5 scraper edits + delete `_shared/bsip0_nutrition.py` to restore the legacy `NUTR_LABEL_MAP`. Git-reversible; no data migration. (Reverting is strictly worse — restores the 0.5g collapse.) |

---

## TASK-169 Recalibration family (EV-030 – EV-033 + EV-027/EV-024/EV-026 extensions)

> **ID-remap note (Data Agent, 2026-06-02).** The TASK-169A/169B design doc drafted the four
> NEW recalibration entries as "EV-029…EV-032", but **EV-029 was already assigned** to the
> BSIP0 nutritionList total-fat overwrite (TASK-142A, above). To preserve the append-only,
> never-reuse-an-ID rule, the four new entries are recorded here as **EV-030 (R1 protein
> scale), EV-031 (R3 leanness), EV-032 (R5 graded sat-fat), EV-033 (R6 veg-spread fit)**.
> Mapping for cross-reference: design-R1→**EV-030**, design-R3→**EV-031**, design-R5→**EV-032**,
> design-R6→**EV-033**; design-R2 extends **EV-027**, design-R4/R7 extend the **EV-024/EV-026**
> lineage (recorded as the EV-024/026 v1.1 extension below). All gated behind the single env
> flag `BARI_RECAL_P0` (default OFF → engine is byte-identical to 0.4.1). Source corpora:
> `run_cheese_003` (n=59) + `run_hummus_002` (n=69), measured distributions, 2026-06-02.

### EV-030 — Category-Relative Protein Scale (R1; protein_quality + nutrient_density)

| Field | Value |
|-------|-------|
| **finding_id** | EV-030 |
| **task** | TASK-169 / TASK-169B (R1) |
| **recorded** | 2026-06-02 |
| **signal** | `PROTEIN_SCALE_TABLES` — protein mass scored 0–100 against the *achievable per-category* protein distribution, replacing a single supplement-calibrated breakpoint list `[(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95)]` used in BOTH `score_nutrient_density` and `score_protein_quality` (25% of the composite). Per-category curves anchored so the real top-of-shelf protein reaches ~95 and the shelf median lands ~55–60. Whole-food ceilings (dairy ~11.5g, hummus ~8g) can now differentiate and reach top-of-shelf within their own category. Source/matrix factors (`source_factors`, `PROTEIN_QUALITY_MATRIX_DISCOUNT`) apply unchanged on top. |
| **data_source** | Measured protein distributions: cheese (`run_cheese_003`, n=59) min/Q1/median/Q3/max = 0/4.4/7.9/10.0/23.0 g; hummus/sauce_spread (`run_hummus_002`, n=69) = 0/2.0/7.7/8.3/22.0 g. Worked anchor: cottage 1% 11.5g protein → mass 90.0 (was 56.0). |
| **mechanism** | Per-category breakpoint table looked up exactly like `CALORIE_DENSITY_TABLES`; linear interpolation between breakpoints (same interpolation as today). Categories: `dairy_protein`/cheese, `sauce_spread`/hummus (active this wave); `milk_dairy`, `yogurt`, `bread`, `snack_bar_granola` modelled but frozen (require P2 owner sign-off); `default` = unchanged supplement curve so untouched categories stay byte-identical. |
| **category_scope** | CROSS-CATEGORY (owner-approved TASK-169). **This wave ships cheese + hummus only.** `snack_bar_granola` deliberately keeps the supplement curve (snk-001 = 70/B ceiling untouched). Frozen milk/yogurt/bread curves modelled but NOT shipped until their separately-approved wave. |
| **evidence_strength / tier** | Moderate — the distribution is real and observed; the apex anchor points (e.g. dairy 11g→85, 13g→95) are a documented calibration choice (see design §(a) open question 1). |
| **label_observability** | Fully label-observable — reads `protein_g` (already required) + routed `category`. |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF). Unset → single supplement breakpoint list restored; 0.4.1 byte-identical. No shadow rule — replaces a hard-coded list with a lookup table. |

### EV-031 — Leanness Reward in fat_quality (R3)

| Field | Value |
|-------|-------|
| **finding_id** | EV-031 |
| **task** | TASK-169 / TASK-169B (R3) |
| **recorded** | 2026-06-02 |
| **signal** | A genuinely lean whole-food matrix (low total fat AND low saturated fat) earns POSITIVE `fat_quality` credit instead of the prior flat neutral-50 short-circuit. Lean band = `fat ≤ 3g/100g`; `_leanness_score = clamp(92 − fat×6 − sat×4, 50..95)`; in the lean band the dimension takes `max(penalty_curve, leanness_score)` so a lean product is never worse than the existing penalty curve. Above 3g fat behavior is byte-identical to today (penalty curve only). |
| **data_source** | cottage/white-cheese/veg-spread traces, `run_cheese_003` / `run_hummus_002`, 2026-06-02. Worked: fat-free white cheese (fat 0.3g, sat None) OLD neutral 50 → NEW 92; cottage 1% (1g/0.6g) 83.2 → 83.6 (≈unchanged, intended). |
| **mechanism** | Replaces the two neutral-50 short-circuits (`fat < 0.5g` OR `sat_fat is None`) in `_score_fat_quality_sprint1` / `score_fat_quality`. Modifies the existing dimension function — no shadow rule. |
| **category_scope** | CROSS-CATEGORY (shipped: cheese + hummus this wave). Also nudges veg spreads (helps R6) and any lean food; frozen-category nudges deferred to their wave. |
| **evidence_strength / tier** | Moderate. |
| **label_observability** | Reads `fat_g` + `saturated_fat_g` (already required). |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF) → neutral-50 short-circuits restored. |

### EV-032 — Graded Saturated-Fat Penalty (R5; red-label cap → graded penalty)

| Field | Value |
|-------|-------|
| **finding_id** | EV-032 |
| **task** | TASK-169 / TASK-169B (R5) |
| **recorded** | 2026-06-02 |
| **signal** | Saturated fat above the Israeli MoH red-label threshold (5.0 g/100g, existing `RED_LABEL_THRESHOLDS`) degrades `fat_quality` PROPORTIONALLY rather than via a single composite cliff. Removes `ISRAELI_RED_LABEL_1_SAT_FAT`→55 from `FAT_QUALITY_CAPS`; adds graded `_red_satfat_penalty = clamp(3.0 + (sat−5.0)×2.5, 0..25)` on the fat_quality dimension, landing before the `FAT_QUALITY_FAMILY_BUDGET=8` clamp so it degrades gracefully and never flattens protein differentiation. |
| **data_source** | cottage-9% vs napoleon-16% inversion, `run_cheese_003`, 2026-06-02. cottage 9% (sat ~5.5g): OLD composite cliff 52/C → NEW keeps protein lead (high-C/low-B), above napoleon. napoleon 16% (sat ~10g): penalty ~15.5, correctly remains below cottage. |
| **mechanism** | One cap removed, one penalty added (net-neutral rule count) — modifies existing penalty machinery, no shadow rule. `regulatory_quality` STILL counts the red label (1 label → 60) so the regulatory signal is NOT lost; only the fat-dimension cliff is removed. |
| **category_scope** | CROSS-CATEGORY (shipped: cheese + hummus). Will move milk/yogurt sat-fat — frozen deltas deferred to their wave (P2). |
| **evidence_strength / tier** | Moderate. |
| **label_observability** | Reads `saturated_fat_g` / `red_labels` (already covered). |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF) → `ISRAELI_RED_LABEL_1_SAT_FAT` cap restored, graded penalty inert. |

### EV-033 — Vegetable-Spread Category Fit (R6)

| Field | Value |
|-------|-------|
| **finding_id** | EV-033 |
| **task** | TASK-169 / TASK-169B (R6) |
| **recorded** | 2026-06-02 |
| **signal** | A whole-vegetable spread (matbucha / roasted-pepper / eggplant; legume protein < 3g, whole-veg base, no tahini-dominant signal) is judged on ingredient cleanliness, whole-food base, low energy density, and sodium discipline — NOT protein density. Implemented as a `veg_spread` archetype within `sauce_spread` carrying `VEG_SPREAD_WEIGHTS` (protein_quality 0.10→0.03, nutrient_density 0.15→0.08, calorie_density →0.18, additive_quality →0.16, regulatory_quality →0.08, whole_food_integrity →0.06; sums to 1.0). |
| **data_source** | matbucha / pepper-spread traces 42.8–61.8/D–C, `run_hummus_002`, 2026-06-02. Post-fix (v1.1 model): matbucha 50–60/C → 61–71/B; eggplant 60–69; **none cross 80**. |
| **mechanism** | Re-weight of existing dimensions for the archetype (no new dimension, no new scoring rule). Detection reuses the raw-vs-prepared boundary logic (tahini + sodium + energy, never protein or the word סלט — per `feedback_raw_vs_prepared_boundary`). |
| **category_scope** | `sauce_spread` only (hummus shelf savory/veg-spread tail) — shipped this wave. |
| **evidence_strength / tier** | Moderate. |
| **anti_immunity_guard** | Per `bari_usecase_guardrails_v2`: the re-weight must NOT let an engineered/sodium-heavy spread reach A. P1 model verified: 0 `veg_spread` crosses the 80 ceiling; a sodium-bomb pepper spread stays C/D via regulatory + sodium cap. Guard intact. |
| **label_observability** | Reads `protein_g`, ingredient base, tahini signal, sodium (already covered). |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF) → uniform `sauce_spread` weights restored; `veg_spread` archetype inert. |

### EV-027 extension — Fiber-N/A activation for cheese under BARI_RECAL_P0 (R2)

| Field | Value |
|-------|-------|
| **extends** | EV-027 (TASK-144) — same signal/source/mechanism; this is an ACTIVATION-SCOPE extension only. |
| **task** | TASK-169 / TASK-169B (R2) |
| **recorded** | 2026-06-02 |
| **change** | The EV-027 fiber "absent ≠ zero" re-normalization (65/35 → 100/0 protein-only for `FIBER_NOT_APPLICABLE_CATEGORIES` when fiber is genuinely absent/≤0) is now ALSO gated to `BARI_RECAL_P0` (OR'd with the existing `TASK144_FIXES_ON`, so maadanim behavior is unchanged): `fiber_not_applicable = (TASK144_FIXES_ON or RECAL_P0_ON) and category in FIBER_NOT_APPLICABLE_CATEGORIES and (fiber_raw is None or fiber_raw <= 0)`. |
| **scope** | `dairy_protein` is ALREADY on the EV-027 allowlist → cheese/cottage/white-cheese inherit it. **`sauce_spread` is deliberately NOT added** — hummus is chickpea-based and fiber IS a genuine virtue there. No category added beyond the existing allowlist; only activation for the cheese run. |
| **inclusion_criterion** | A category joins `FIBER_NOT_APPLICABLE_CATEGORIES` only if near-zero fiber is the structurally correct, expected value for the WHOLE category (fiber-free animal/dairy matrix). Bread/cereal/bars/crackers/sauces/spreads/beverages stay excluded (missing fiber there is a real deficiency). |
| **evidence_strength / tier** | Strong (parallels the owner-approved whole-food-fat-floor principle). |
| **rollback_flag** | `BARI_RECAL_P0` (and/or `BARI_TASK144_FIXES`) OFF → flat 65/35 blend with fiber-as-0 returns. |

### EV-024 / EV-026 lineage extension (v1.1) — NOVA flavored-variant guard (R4) + culture-gate (R7), under BARI_RECAL_P0

| Field | Value |
|-------|-------|
| **extends** | EV-024 (culture-credit) + EV-026 (data-hygiene) lineage — the plain-dairy / culture family. REVISED per design v1.1. |
| **task** | TASK-169 / TASK-169B (R4 + R7) |
| **recorded** | 2026-06-02 |
| **R4 signal** | Benign culinary/culturing/fortification additions to a plain dairy base keep NOVA 2 (demote a tentative NOVA 3 back to 2) — **BUT a declared flavoring, even a whole-food one (garlic/dill/herbs/etc.), makes it a flavored variant and forfeits the retention → stays NOVA 3.** New `FLAVORED_VARIANT_MARKERS_HE` list feeds an added `has_flavor_variant` clause in the `nova_proxy.py` `is_plain` gate. Guard ONLY ever BLOCKS a demotion (can only lower, never raise a score). Retires the false "מבנה רכיבים מעובד" line for products that legitimately pass to NOVA 2. |
| **R7 signal** | The +8 `FERMENTATION_DIRECT_BONUS` fires only on **(A)** a declared culture marker (`has_fermentation`, existing/unchanged) **OR (B)** an inherently-cultured product TYPE — yogurt subtype, or aged/specialty cultured-cheese NAME marker. **Fluid milk (`milk_dairy` / fluid-milk name tokens) and plant drinks are HARD-EXCLUDED.** The v1 "plain-dairy ⇒ cultured" assumption is RETRACTED as unsound (it credited uncultured fluid milk — the 85/A milk-ceiling leak — and over-credited table-stakes fresh-cheese culturing). Plain cottage/white-cheese fresh subtypes are deliberately EXCLUDED from Path B (they reach the owner's 90/A target from R1+R2+R4 alone; +8 would overshoot to ~97/S). |
| **router-reconciliation** | Live router emits NO `milk_dairy` or top-level `yogurt` category — fluid milk, yogurt and cheese all route as `dairy_protein`. Implemented against the real router vocabulary: yogurt qualifies via real yogurt SUBTYPES; fluid milk hard-excluded by a token-aware fluid-milk NAME marker lacking a dairy-solid identity marker (חלב-vs-חלבון substring trap fixed by whole-token matching); aged/specialty cheese qualifies by NAME marker. New routing allowlists: `CULTURED_YOGURT_SUBTYPES`, `CULTURED_CHEESE_NAME_MARKERS_HE`, `FLUID_MILK_NAME_MARKERS_HE`, `DAIRY_SOLID_IDENTITY_MARKERS_HE`. |
| **data_source** | cottage NOVA 2→3 regression (run_001 vs run_003); napoleon שום שמיר flavored-A leak; both fluid-milk +8 leaks — all `run_cheese_003`/model 2026-06-02. |
| **category_scope** | CROSS-CATEGORY behind the flag; shipped this wave for cheese + hummus. Yogurt retains its (legitimately gated) bonus but yogurt is FROZEN this wave (not rescored/reshipped). Milk leak closed but milk is FROZEN (deferred). |
| **evidence_strength / tier** | Moderate. Path A fully label-observable; Path B is product-type/name-derived (reconciled against live routing). R4 is name + ingredient substring. |
| **rule_accumulation** | No new rule, no shadow rule: R7 v1.1 NARROWS an existing bonus path (fewer products qualify); R4 v1.1 ADDS ONE disqualifier clause to an existing demotion guard. Net rule count unchanged; blast radius strictly smaller than the v1 model. New constants are routing allowlists / marker lists feeding existing tests. |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF). Unset → v1 R7 path (`product_type_dairy + plain ⇒ +8`) and v1 R4 `is_plain` (additive-marker-only) restored; 0.4.1 byte-identical. |

---

### EV-034 — Yogurt +8 A-Ceiling (S reserved; reserve-the-apex trim under BARI_RECAL_P0_YOGURT_TRIM)

| Field | Value |
|-------|-------|
| **finding_id** | EV-034 |
| **concept** | A cultured yogurt lifted by the gated live-culture **+8** (EV-015 / R7, Path B `yogurt_subtype`) MAY reach grade **A** but cannot, by the +8 alone, manufacture an **S**. The +8's reach is ceiling-capped at the top of the A band so the rare S grade stays reserved. Yields **15 A / 0 S** vs the un-trimmed 11 A / 3 S (the cap moves exactly the 3 former-S → A; the +1 over the 14 first projected is a separate legitimate data-hygiene restore — bio-naturel regained its real +8 → 85.5/A, not a cap effect). |
| **scientific_rationale_short** | The 3 S-grade yogurts are not nutritionally exceptional — they are engineered high-protein "GO/חלבון" SKUs whose already-high base is pushed over 90 by the +8 culture bonus. The +8 is an EV-015 fermentation credit (mineral bioaccessibility, organic-acid glycemic dampening, restructured protein); it is a genuine positive, but it is a *category-defining table-stakes* positive shared by every cultured yogurt, not an apex differentiator. Letting a shared bonus stack into the platform's strongest grade rewards protein fortification (G-014: protein density ≠ quality) over the cultured-dairy matrix itself. Per the frozen "best ≠ excellent" doctrine, the top of a maturing shelf should be a rich A-tier, with S withheld until a genuinely exceptional case appears. The cap is set at **89.9** = the top of the A band (grade boundaries: S ≥ 90, A 80–89.99), so a +8-lifted yogurt lands at 89.9/A — the maximum the bonus can earn without claiming an unearned apex. |
| **evidence_strength** | Moderate — directional rationale is Strong (composes EV-015 fermentation + G-014 protein-quality guardrail + frozen milk/cheese ceiling discipline); the *exact* cut (89.9 vs a lower A-internal value) is a calibration judgement, owner-set, flagged for Product co-sign. |
| **confidence_level** | High (on the mechanism + surgicality; verified 86/86 corpus) |
| **BSIP2_relevance** | Direct — governs the apex of the yogurt shelf under the TASK-169 recal. Without it, recal publishes 3 S (one of which is a corrupt-data artifact, 190 g protein/100 g). With it, the shelf tops out at a 14-product A-tier and S is held in reserve. |
| **implementation_complexity** | Low — no new signal, no new rule path; a post-bonus clamp on `weighted_dim_score` scoped to recipients of the existing R7 `yogurt_subtype` +8. |
| **recommended_action** | governance_ruling — **owner-set intent (TASK-169D, 2026-06-03); Product Agent D7 co-sign REQUIRED before P1/ship** (new scoring construct, not yet co-signed). |
| **affected_categories** | `dairy_protein` — **yogurt subtypes ONLY** (R7 Path B `yogurt_subtype`). Does NOT touch milk, cheese, hummus, or any other category. Distinct from the cheese A-ceiling (EV-021 A1): cheese gates A on a sodium+sat-fat cleanliness predicate; this gates the apex on the *source of the lift* (the +8), not a nutrition floor. |
| **candidate_signal_name** | (no new signal — clamps the EV-015 `fermentation_quality_bonus` contribution via `RECAL_P0_YOGURT_TRIM_CEILING`) |
| **predicate** | `if RECAL_P0_YOGURT_TRIM and r7_culture_credit and r7_path == "yogurt_subtype" and weighted_dim_score > 89.9: weighted_dim_score = 89.9` — applied post-bonus, pre-floor, in `score_engine.py`. Constant `RECAL_P0_YOGURT_TRIM_CEILING = 89.9`. |
| **threshold_grounding** | 89.9 = the S/A boundary minus the engine's 2-dp resolution; it is the *highest* A-band value, so it preserves the full A-tier lift the recal intends while removing exactly the S-crossing. It is a clamp at the grade boundary, NOT a derived nutrition threshold — chosen because the harm being corrected is "an A-grade product crossing into S purely on a shared bonus," which is a boundary phenomenon, not a composition phenomenon. Surgical proof: moves exactly the 3 S→A (GO lactose-free, GO 25g, יופלה GO), 0 collateral on the other 83 SKUs. |
| **should_affect_score_now** | false — flag-gated decision construct; Product D7 co-sign + the two corpus data fixes (corrupt 190 g protein SKU; bio-naturel false +8 exclusion) are prerequisites before any rescore is published. No live score moves from this entry. |
| **required_input_fields** | (consumes existing) `r7_culture_credit`, `r7_path`, `weighted_dim_score` |
| **risk_of_misuse** | (1) Mistaking this for a nutrition-floor S-gate — it is a boundary clamp on a bonus-driven apex, not a quality assessment; do NOT generalize it into "yogurt can never be S." A future genuinely-exceptional yogurt reaching the A band on the protein/density scale *without* needing the +8 to cross 90 is unaffected. (2) Applying it to cheese/milk — it is yogurt-subtype-scoped by the R7 path key. (3) Treating the corrupt 190 g/100 g SKU's cap as a fix for the bad data — it is not; the data must be corrected/withheld independently (the cap merely prevents the artifact from topping the shelf as an S). |
| **gated_by** | `BARI_RECAL_P0_YOGURT_TRIM` (default OFF), itself inert unless `BARI_RECAL_P0` is ON. |
| **rollback** | Unset `BARI_RECAL_P0_YOGURT_TRIM` → option (a) behavior (11 A / 3 S) restored; flag-OFF rescore is 86/86 byte-identical to the recal baseline (the trim flag is fully inert when set OFF, and inert when `BARI_RECAL_P0` is OFF). Golden + router clean OFF / ON / ON+TRIM. Notify: Nutrition (EV-015/EV-021 owner) + Product (D7 co-signer). |
| **precedent** | EV-021 Amendment A1 (cheese A-ceiling) — same "reserve the apex on a maturing shelf" discipline and same `BARI_RECAL_P0` rollback family; differs in mechanism (cheese = nutrition-cleanliness predicate; yogurt = bonus-reach clamp at the grade boundary). |
| **status** | Owner-approved intent (TASK-169D); **Product D7 CO-SIGNED 2026-06-03 (Product Agent)** — clears P1/ship. Recorded 2026-06-03. |
| **product_d7_cosign** | CO-SIGN (2026-06-03). Confirms: (1) Policy — S is reserved on the yogurt shelf; a +8-driven cultured yogurt tops out at A (89.9), net 15 A / 0 S vs 11 A / 3 S uncapped. (2) Scope — yogurt-subtype-only, flag-gated, byte-identical rollback (86/86), moves exactly the 3 former-S to A, 0 collateral; the +1 to 15 A is a legitimate separate data-hygiene restore (bio-naturel +8 → 85.5/A), NOT a cap artifact. (3) Ship-gating chain satisfied — corpus fixes done (190g→12.5 OFF-sourced; bio-naturel false +8 fixed), clean HEAD rescore done (run_yogurt_006_recal_p0_trim), Nutrition EV authored + endorsed. Mechanism (A-ceiling on the +8's reach) is the correct lever per G-014 + "best ≠ excellent"; consistent with EV-021 A1 cheese-ceiling discipline. CONDITION: reconcile the EV-034 concept field's "14 A / 0 S" headline to the authoritative **15 A / 0 S** (the +1 is the legitimate bio-naturel restore). Standing approval is for option (b) cap; any future move OFF the cap (toward 11A/3S) is a NEW D7 + Nutrition gate, not covered here. |
| **notes** | Source: TASK-169D + `02_products/yogurt_system/bsip2_outputs/run_yogurt_005_recal_p0/DECISION_PACKAGE.md` (run id `run_yogurt_005_recal_p0`, config hash `38654862b46baaac`, corpus run_yogurt_003 n=86). The literal "R1 yogurt anchor" trim was investigated and REJECTED as the lever: the dedicated yogurt protein scale is more generous at the typical-yogurt midrange and would *raise* the A-count (~25 A), not trim the top — the apex over-reach is the +8 stacking, so the A-ceiling on the +8 is the correct lever. See also the culture-gate honey-text data fix (EV-024/026 lineage) which must land so plain bio yogurt is not falsely denied the +8. |

---

### EV-031 / EV-032 — TASK-169F bread blast-radius CONFIRMATION (estimate → modeled)

| Field | Value |
|-------|-------|
| **extends** | EV-031 (R3 leanness) + EV-032 (R5 graded sat-fat). No new rule, no new signal, no parameter change — this entry RECORDS the modeled bread blast radius that TASK-169A could only ESTIMATE (bread used a bespoke loader not wired into the recal harness). |
| **task** | TASK-169F (frozen bread wave) |
| **recorded** | 2026-06-04 |
| **wiring** | `real_bread_retail_003_v1` wired into the recal harness by reusing the real runner `batch_run_bread_retail_003.py` as a module (`normalize_to_bsip1` + full `run_pipeline`, incl. synthesis + confidence ceiling), toggling ONLY `BARI_RECAL_P0` OFF→ON on the SAME HEAD engine. Artifact: `02_products/bread_retail_003/_model_task169f/run_169f_bread_recal.py`. Corpus = the 31 curated products (24 displayed + 7 transparency-only). |
| **R3 modeled effect (bread)** | The bespoke bread loader sets `fat_saturated_g = None` for ALL bread, so R3 fires via the **`sat_fat is None`** branch → `_leanness_score(fat, 0.0)`. fat_quality dimension rises from the legacy neutral **50.0 → 80–92** for every bread (lean matrix). Net final-score effect is SMALL and BOUNDED: 14/31 move, 4 grade-affecting B→A, 10 cosmetic (<2pt, no grade change), 17 unmoved. The large dim jump is absorbed by the **moderate-confidence band score ceiling (82)** that all CAUTIOUS bread sits under — no bread exceeds 82, none reaches S. "best ≠ excellent" framing intact. |
| **R5 modeled effect (bread)** | **INERT for bread.** `_red_satfat_penalty` requires `sat_f > 5.0g`; bread's `fat_saturated_g` is `None` for 31/31 → 0 sat-fat red labels → penalty = 0 across the whole corpus. The recal cliff→slope change has NO bread effect. |
| **R1/R2/R4/R6 (confirmed not materially applicable)** | R1 bread protein curve: deliberately conservative (bread not rewarded as a protein food); no grade move attributable to it in the corpus. R2 fiber-N/A: bread is DELIBERATELY EXCLUDED from `FIBER_NOT_APPLICABLE_CATEGORIES` (missing fiber in bread IS a real deficiency). R4 NOVA flavored-variant: dairy-scoped; **0/31 NOVA changes OFF→ON** (verified). R6 veg_spread: `sauce_spread`-only archetype; bread does not route there. CONFIRMED, not assumed. |
| **drift separation (TASK-178)** | OFF reproduces only **6/24** of the published build-time bread scores — an 18/24 pre-existing HEAD-vs-build-time engine DRIFT (TASK-178 domain), NOT a recal effect. Because the recal delta is OFF→ON on the SAME HEAD engine, that drift appears identically in both columns and CANCELS; `delta_recal = on − off` is pure recal. The harness reports `head_drift_vs_live` separately and never folds it into the recal delta. |
| **safety contract** | Flag-OFF determinism verified (`verify_169f_off_identical.py` CHECK 1 PASS — every R3/R5 branch is `if RECAL_P0_ON`, so OFF cannot enter a recal path). Golden regression 11 PASS / 1 WARN / 0 FAIL flag-insensitive (no bread in golden set; WARN = pre-existing `anchor_soy_drink`). Router 13/13 PASS OFF and ON. |
| **status** | MODEL ONLY — NOT shipped. The 4 frozen bread B→A moves require **explicit owner per-move P2 sign-off** before any rescore/reship (P3). Bread provenance `real_bread_retail_003_v1` is a frozen invariant; this entry recommends, it does not move a live score. |
| **rollback_flag** | `BARI_RECAL_P0` (default OFF) — unchanged from EV-031/EV-032. |

---

### EV-035 — D5 Disclosure-Gap Taxonomy (five types) over the raw BSIP0 panel

| Field | Value |
|-------|-------|
| **finding_id** | EV-035 (Glass Box Wave 1, D5; relocated from governance draft EV-079 — TASK-179F) |
| **task** | TASK-179D / TASK-179F (Glass Box D5/D6 Wave 1) |
| **recorded** | 2026-06-04 |
| **signal** | Five deterministic disclosure-gap detectors over the raw BSIP0 panel: G1 undisclosed proportions (with single-ingredient protection), G2 compound-without-breakdown, G3 protein blend / unspecified source (collagen/gelatin routed to D2, not a gap), G4 generic additive class without E-code/name, G5 declared-quantity-missing (names the field; no re-deduction of the legacy six). The structural-vs-closable severity split drives the D5-band. Per Q2/DEC-006 the taxonomy produces a **disclosure profile only** and **never deducts grade points** — it feeds D6 (confidence) and annotation only. |
| **data_source** | Detectors run on `ingredients_raw` + `nutrition` from `02_products/*/...bsip0_raw*.json` after P1 nutrition-bleed truncation and P2 Hebrew normalization. **P3 panel-present is TOKEN-AWARE** (TASK-179L, 2026-06-04): a panel counts as present when it carries ≥1 coherent ≥2-letter Hebrew ingredient token after P1 (NOT a character-length cutoff), so a short clean single-ingredient panel (`אגוזי מלך`, `שקדים`) is present → `single_ingredient` → full band, never wrongly withheld; only blank/garbage panels read absent. Faithful to single-ingredient protection; pilot-verified (hummus withholds 7→4, all 3 recovered keep grade). Nutrition D6/D7 co-signed. |
| **mechanism** | Deterministic ingredient/panel detectors emitting a disclosure profile + D5-band; no quality-point deduction. Builds on EV-029 (Hebrew final-letter parser trap). |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF). |
| **evidence_strength / tier** | Moderate — deterministic taxonomy; severity calibration is a documented choice revisitable after the pilot flag-ON diff. |
| **label_observability** | Fully label-observable — reads `ingredients_raw` + `nutrition` (raw BSIP0 panel only; EDPG firewall — no external value read directly). |
| **co_sign** | Nutrition D6/D7 — co-signed (TASK-179F, 2026-06-04). Product D7 — co-signed (TASK-179E, 2026-06-04); D7 formal close 2026-06-05 (D5/D6 operative post Glass Box W4 ship). |
| **fidelity** | Q2: disclosure profile only, never a grade-point deduction; feeds D6 + annotation. |
| **status** | Active — co-signed Product D7 2026-06-05. Adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF; OFF = byte-identical; revisitable after the pilot flag-ON diff). |
| **source** | `01_framework/glass_box/d5_d6_rule_spec_v1.md §1`; six-dimension contract §D5; TASK-179A §1–§3 disclosure observations; EV-029 (Hebrew final-letter parser trap). |
| **rollback_flag** | `BARI_GLASSBOX_D5D6` (default OFF) — unset → no D5 profile produced; engine byte-identical. |

---

### EV-036 — Endemic-Flavoring Exclusion from the D5 band

| Field | Value |
|-------|-------|
| **finding_id** | EV-036 (Glass Box Wave 1, D5; relocated from governance draft EV-080 — TASK-179F) |
| **task** | TASK-179D / TASK-179F (Glass Box D5/D6 Wave 1) |
| **recorded** | 2026-06-04 |
| **signal** | Bare `חומרי טעם וריח` is present in ~70% of maadanim panels (129/184). To avoid a category-blind distortion (cf. DISTORTION-001 dairy-fiber), bare flavorings are recorded in the disclosure profile as `endemic_flavoring` and annotated with a calm, non-intent note ("הרכב הטעמים לא פורט"), but are EXCLUDED from D5 band-raising and therefore from the D6 confidence reduction. |
| **data_source** | maadanim BSIP0 frequency analysis 2026-06-04 (129/184 panels). |
| **mechanism** | Endemic-flavoring marker excluded from band-raising; annotation-only. Re-evaluate per `cereals_gap_resolution_v1 §6.4` (endemic-distortion protocol) if a future category shows flavorings are not endemic. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF). |
| **evidence_strength / tier** | Moderate — endemicity is the documented basis; revisitable per §6.4. |
| **label_observability** | Fully label-observable — reads `ingredients_raw`. |
| **co_sign** | Nutrition D6/D7 — co-signed (TASK-179F, 2026-06-04). Product D7 — co-signed and explicitly backed (TASK-179E, 2026-06-04); D7 formal close 2026-06-05. |
| **fidelity** | Q2: annotation-only; never raises the band, never reduces confidence. |
| **status** | Active — co-signed Product D7 2026-06-05. Adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF; OFF = byte-identical; revisitable after the pilot flag-ON diff). |
| **source** | `01_framework/glass_box/d5_d6_rule_spec_v1.md §1.4`; maadanim BSIP0 frequency analysis 2026-06-04; `cereals_gap_resolution_v1 §6.4`. |
| **rollback_flag** | `BARI_GLASSBOX_D5D6` (default OFF). |

---

### EV-037 — D5-band → D6 Confidence Reduction (partial −10 / severe −20 / structural-only 0)

| Field | Value |
|-------|-------|
| **finding_id** | EV-037 (Glass Box Wave 1, D6; relocated from governance draft EV-081 — TASK-179F) |
| **task** | TASK-179D / TASK-179F (Glass Box D5/D6 Wave 1) |
| **recorded** | 2026-06-04 |
| **signal** | The D5-band feeds D6 as a single named reduction inside the existing `compute_confidence` accumulator, gated by the flag: full 0, **minor 0** (structural-only gaps are the market floor — "buy coverage over silence" — and do not erode confidence), **partial −10**, **severe −20**. Structural gaps never reduce confidence; only closable opacity (a name/E-code the manufacturer could have disclosed and did not) does, and even then modestly — so D5 acts *through* confidence, never as a back-door quality penalty (Q2). No double-count with the legacy missing-field map (G5 names the legacy six but does not re-deduct). |
| **data_source** | six-dimension contract §D6, D-CONF-1; `confidence_framework.md` (BEV-018/BEV-019). |
| **mechanism** | Single named reduction term inside the existing `compute_confidence` accumulator. **This reduction is the source of essentially all ON-vs-OFF score movement** (alongside the panel-absent null flip in EV-038); both are demote-or-null only, never promotion. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF). |
| **evidence_strength / tier** | Moderate — the −10/−20 are starting values, revisitable after the pilot flag-ON diff. |
| **label_observability** | Fully label-observable — consumes the EV-035 D5-band (raw-panel-derived). |
| **co_sign** | Nutrition D6/D7 — co-signed the −10 / −20 / structural-only-0 values (TASK-179F, 2026-06-04). Product D7 — co-signed (TASK-179E §3&4, 2026-06-04); D7 formal close 2026-06-05. |
| **fidelity** | Q2: acts through confidence only, never a back-door quality penalty; demote-or-null only, never promotion. |
| **status** | Active — co-signed Product D7 2026-06-05. Adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF; OFF = byte-identical; the −10/−20 are starting values, revisitable after the pilot flag-ON diff). |
| **source** | `01_framework/glass_box/d5_d6_rule_spec_v1.md §2.1`; six-dimension contract §D6, D-CONF-1; `confidence_framework.md` (BEV-018/BEV-019). |
| **rollback_flag** | `BARI_GLASSBOX_D5D6` (default OFF) — unset → no D5-derived confidence reduction. |

---

### EV-038 — D6 Gate State Machine + Null-vs-Cap Floor (`NULL_FLOOR=30` AND-severe; `DEMOTE_CEILING_BOUND=60` no-op)

| Field | Value |
|-------|-------|
| **finding_id** | EV-038 (Glass Box Wave 1, D6; relocated from governance draft EV-082 — TASK-179F) |
| **task** | TASK-179D / TASK-179F (Glass Box D5/D6 Wave 1) |
| **recorded** | 2026-06-04 |
| **signal** | Extends the existing confidence ceiling from ceiling-only to a three-state gate `unconstrained · demote · withhold(→null)`. **`DEMOTE_CEILING_BOUND=60` is a NO-OP restatement of the live confidence band edge — it changes no behavior on its own.** The live constants `CONFIDENCE_LOW_CEILING=75` (applied 40–59) and `CONFIDENCE_INSUFFICIENT_CEILING=50` (applied <40) are **unchanged**; `demote` simply reuses them plus a visible `ניתוח חלקי` flag and carries the normal partial-disclosure case (Q1 conservative-to-demote). `withhold(→null)` (`score:null`, label `לא נוקד`) fires ONLY on a floor-of-observability failure: panel absent, OR `d6_confidence < 30` AND a `severe` D5-band (Q1 reluctant-to-withhold — buy coverage over silence). |
| **data_source** | six-dimension contract §D6, §2.6, §2.7, §5.0 Q1; DEC-006; `confidence_framework.md` (BEV-018); `constants.py` (`CONFIDENCE_LOW_CEILING=75`, `CONFIDENCE_INSUFFICIENT_CEILING=50`). |
| **mechanism** | Three-state gate over the existing ceiling. **ALL ON-vs-OFF behavioral movement originates in EV-037's −10/−20 confidence reduction plus the panel-absent→null flip — both demote-or-null only, never promotion; the bound `60` itself moves nothing.** D6 can never raise a score, preserving the frozen invariants. The numbers 30 and 60 are starting values. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF). |
| **evidence_strength / tier** | Moderate — `30` and `60` are starting values, revisitable after the pilot flag-ON diff. |
| **label_observability** | Fully label-observable — consumes D6 confidence + EV-035 D5-band + panel-present flag. |
| **co_sign** | Nutrition D6/D7 — co-signed `DEMOTE_CEILING_BOUND=60` (no-op restatement) and `NULL_FLOOR=30` gated on severe-AND-confidence<30, or panel-absent (TASK-179F, 2026-06-04). Product D7 — co-signed with the required wording fix applied above (TASK-179E §1, 2026-06-04); D7 formal close 2026-06-05. |
| **fidelity** | Q1: conservative-to-demote on partial disclosure; reluctant-to-withhold (buy coverage over silence). Demote-or-null only, never promotion. |
| **status** | Active — co-signed Product D7 2026-06-05. Adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF; OFF = byte-identical; `30` and `60` are starting values, revisitable after the pilot flag-ON diff). |
| **source** | `01_framework/glass_box/d5_d6_rule_spec_v1.md §2.2–§2.3`; six-dimension contract §D6, §2.6, §2.7, §5.0 Q1; DEC-006; `confidence_framework.md` (BEV-018); `constants.py` (`CONFIDENCE_LOW_CEILING=75`, `CONFIDENCE_INSUFFICIENT_CEILING=50`); Product co-sign wording requirement (TASK-179E §EV-append condition 2). |
| **rollback_flag** | `BARI_GLASSBOX_D5D6` (default OFF) — unset → ceiling-only behavior restored; no null-floor flip. |

---

### EV-039 — `BARI_GLASSBOX_D5D6` Flag + OFF = byte-identical guarantee

| Field | Value |
|-------|-------|
| **finding_id** | EV-039 (Glass Box Wave 1; relocated from governance draft EV-083 — TASK-179F) |
| **task** | TASK-179D / TASK-179F (Glass Box D5/D6 Wave 1) |
| **recorded** | 2026-06-04 |
| **signal** | All D5/D6 logic is gated by env flag `BARI_GLASSBOX_D5D6` (default OFF). With OFF the engine output and the golden/frozen runs are 0-diff vs the pre-D5/D6 baseline (same discipline as `BARI_RECAL_P0` / `BARI_TASK144_FIXES`). With ON, the only possible score-moving deltas are demotions (band-edge ceiling shifts driven by the EV-037 reduction) and `insufficient_data`→`לא נוקד` flips — never promotions. |
| **data_source** | `score_engine.py` flag pattern (`BARI_RECAL_P0`, `BARI_TASK144_FIXES`); six-dimension contract §4 invariant-preservation. |
| **mechanism** | Single env-flag gate; OFF = byte-identical, ON = demote/null only. Rollback = unset the flag. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF). |
| **evidence_strength / tier** | Strong (flag discipline parallels the validated `BARI_RECAL_P0` / `BARI_TASK144_FIXES` pattern). |
| **label_observability** | N/A — engineering invariant. The frozen runs (milk `run_004_recalibrated`, snack-bars `snk-001=70/B`, bread `real_bread_retail_003_v1`) must re-verify 0-diff OFF and demote/null-only ON at the separate pilot gate (QA, TASK-179 wave). |
| **co_sign** | Nutrition D6/D7 — co-signed (TASK-179F, 2026-06-04). Product D7 — co-signed (TASK-179E §EV-append condition 3, 2026-06-04); D7 formal close 2026-06-05. |
| **fidelity** | OFF = byte-identical; ON = demote-or-null only, never promotion; frozen invariants preserved. |
| **status** | Active — co-signed Product D7 2026-06-05. Adopted-behind-flag (`BARI_GLASSBOX_D5D6`, default OFF; OFF = byte-identical; revisitable after the pilot flag-ON diff). |
| **source** | `01_framework/glass_box/d5_d6_rule_spec_v1.md §2.4, §4`; six-dimension contract §4 invariant-preservation; `score_engine.py` flag pattern (`BARI_RECAL_P0`, `BARI_TASK144_FIXES`). |
| **rollback_flag** | `BARI_GLASSBOX_D5D6` (default OFF) — unset = rollback. |

---

### EV-040 — DIAAS Protein Source Quality Signal (D2 credit / D5 disclosure flag, W1.5)

| Field | Value |
|-------|-------|
| **finding_id** | EV-040 (Glass Box W1.5, D2 credit + D5 disclosure flag; TASK-179P) |
| **task** | TASK-179P (Glass Box W1.5) |
| **recorded** | 2026-06-04 |
| **signal** | Two rules govern protein-source quality assessment in the Glass Box engine. **Rule A (D2 complete-protein credit):** when a product's ingredient panel explicitly names a single protein source that is complete (DIAAS ≥ 75 per the diaas_source_table_v1.md Research table — whey/WPI, casein, egg, egg white, soy protein isolate/SPI only), award a mild D2 ingredient-evidence credit of **+3 raw score points** (bounded to ≤ 0.5 grade band, approximately ≤ 3–4 raw score points). This credit is a signal that the protein source is scientifically validated as complete, not a reward for marketing. SPI-specific constraint: Rule A applies only to the declared term "חלבון סויה מבודד" or equivalent isolate language; generic "סויה" or "קמח סויה" (soy flour, DIAAS ~55–65) does not qualify. **Rule B (D5 disclosure gap flag):** when a product declares only a generic protein term without a single named source — specifically "תערובת חלבונים," "חלבון צמחי," "מי גבינה" (generic without "מבודד"), or a multi-source blend without proportions (canonical pea+rice case) — emit a D5 disclosure-gap annotation ("פרטי החלבון לא הופיעו בתווית") plus a D6 confidence reduction using the existing EV-037 partial-disclosure mechanism (−10 if this gap creates or worsens a partial D5-band). Rule B does NOT penalize a product for having incomplete protein. It flags that Bari cannot evaluate protein quality because the label does not disclose the source. |
| **data_source** | `01_framework/glass_box/diaas_source_table_v1.md` (Research Phase 1, TASK-179P); FAO/WHO (2013) Food and Nutrition Paper 92; PMID 28382889 (Brouns/BJN 2017); PMID 33133540 (2020); PMID 39703894 (2024); PMID 40075933 (2025). |
| **mechanism** | Rule A fires in the D2 ingredient-evidence sub-score when the ingredient panel, after P2 normalization, contains exactly one named protein source from the whitelist {חלבון מי גבינה מבודד, חלבוני מי גבינה, קזאין, חלבוני חלב, חלבוני גבינה, ביצה שלמה, ביצים, חלבון ביצה, חלבון סויה מבודד}. Magnitude: **+3 raw score points** to the D2 sub-score, applied behind flag `BARI_GLASSBOX_W15`. Rule B fires in the D5 gap detector as a G3 structural gap when the panel contains any generic protein term from the trigger set {תערובת חלבונים, חלבון צמחי, מי גבינה (without מבודד qualifier), multi-source blends without proportions}; routes to D5 profile annotation and, if the D5-band reaches partial or worse, feeds the EV-037 −10 D6 reduction. Both rules gated by `BARI_GLASSBOX_W15` (default OFF); OFF = byte-identical to engine-baseline-2026-06-04. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_W15`, default OFF). Applicable wherever protein sources are declared: hummus, maadanim, yogurt, snack bars, dairy. |
| **evidence_strength / tier** | Rule A (D2 credit): **Strong** — the completeness classification for whey, casein, egg, and egg white is based on multiple independent pig-model DIAAS studies and FAO/WHO 2013 benchmark endorsement. SPI classification is **Strong** for the isolate form (DIAAS 78–98 in pig models; the ≥75 threshold is met robustly). Rule B (D5 flag): **Strong** — the non-disclosability of pea+rice blend ratios on Israeli labels is a structural market fact; the G3 gap type is already defined in EV-035 and confirmed empirically across the corpus. |
| **label_observability** | Partially label-observable. The protein source name is observable when declared (Rule A applies). Protein quality (DIAAS) is never directly observable from the label — Rule A credits the disclosed source against a curated reference table, not a per-product measurement. Multi-source blends (Rule B) are observable as a pattern; the blend ratio is structurally unobservable from Israeli labels. The pea+rice blend case is the canonical D5 structural gap. |
| **co_sign** | Nutrition D7 — co-signed 2026-06-04 (Rule A magnitude +3 and whitelist; Rule B trigger set; soy-form and pea+rice edge cases). Rule A magnitude (+3) requires Product D7 co-sign before engine activation (it moves a D2 sub-score and could affect the headline grade in borderline cases). Rule B is a D5 annotation + existing D6 path — no standalone grade movement; this portion does not require a separate Product co-sign beyond the existing EV-037 sign-off. |
| **fidelity** | Flag OFF = byte-identical; engine baseline-2026-06-04 unaffected. Flag ON = Rule A awards +3 D2 sub-score credit for declared complete protein source; Rule B adds D5 annotation for generic protein terms. No grade movement is live until Product co-signs Rule A magnitude. Frozen invariants preserved: milk scores (run_005_headpin) not affected (dairy proteins already declared explicitly and would gain +3 D2, which does not threaten the S/A ceiling; the snack-bar ceiling 70/B is structurally safe because +3 D2 cannot alone lift a bar to A). |
| **status** | Adopted-behind-flag (`BARI_GLASSBOX_W15`, default OFF; not live-active). Rule A magnitude requires Product D7 co-sign before engine activation. Rule B (D5 annotation + D6 path) has no standalone grade effect and inherits existing EV-037 approval. |
| **source** | `01_framework/glass_box/diaas_source_table_v1.md`; `01_framework/glass_box/six_dimension_contract_v1.md` §D2/D5; `01_framework/glass_box/d5_d6_rule_spec_v1.md` §1.2 G3; EV-035 (G3 protein-blend gap type); EV-037 (D5-band → D6 reduction). |
| **rollback_flag** | `BARI_GLASSBOX_W15` (default OFF) — unset → no D2 credit, no Rule B annotation beyond existing G3 path. |

---

### EV-041 — D4 Additive-Tier Detector (6-tier model; W2 presentation-only; W3 demand-gated)

| Field | Value |
|-------|-------|
| **finding_id** | EV-041 (Glass Box Wave 2, D4; TASK-179S implementation + TASK-179Q prototype set) |
| **task** | TASK-179S (engine implementation); TASK-179Q (20-additive prototype set + D7 co-sign) |
| **recorded** | 2026-06-04 |
| **dimension** | D4 — additive evidence |
| **signal** | A per-product `d4_additives` array listing every named additive detected in the ingredient text that is present in the 20-additive prototype set, with its tier, Hebrew name, and technological function. Each entry carries `e_number`, `name_he`, `tier`, `function_he`, and `match_source` (`e_number` / `name_he` / `both`). Additives in the ingredient text that are not in the prototype set are emitted with `tier: "unclassified"` — no tier verdict. Additives absent from the text are not emitted. |
| **tier_model** | 6 operational tiers + 1 no-match fallback: **(1) `functional`** — well-characterised function, broad regulatory acceptance, no safety concern at typical food doses; **(2) `likely-neutral`** — extensive history of use, no significant safety signal in current evidence at typical doses; **(3) `dose-dependent`** — safe at typical food doses; concern arises at high or cumulative exposure levels; **(4) `contested`** — mixed or emerging evidence; mechanistic signals present without consensus; benefit of the doubt per DEC-006; **(5) `disclosure-gap`** — insufficient published evidence to assign a tier; present on shelves but understudied; **(6) `confirmed-negative`** — credible signal of harm at relevant exposure levels, supported by regulatory scrutiny or controlled evidence; **(7) `unclassified`** — no-match fallback only; additive detected but not in the prototype set; not a tier verdict. The tier model is frozen from the D7 co-signed `additive_prototype_set_v1.md` (TASK-179Q). |
| **source_of_truth** | `01_framework/glass_box/additive_prototype_set_v1.md` — the 20-additive prototype set, D7 co-signed via TASK-179Q (Nutrition + Product, 2026-06-04). This sheet is the only tier input for W2. Tier assignments are not derived from this registry entry; this entry records them. |
| **w2_scope** | **Presentation-only.** The `d4_additives` array is purely additive to the per-product result dict. It does NOT affect `score`, `grade`, any gate field, or any existing result field. The engine is byte-identical to the `BARI_GLASSBOX_D5D6` baseline when `BARI_GLASSBOX_W2=off` (verified by `verify_glassbox_w2_off_identical.py`, TASK-179S deliverable). No score movement, no grade change. |
| **w3_demand_gate** | **D4 score movement is explicitly gated on TASK-179X (W2 engagement gate) passing.** The W2 engagement gate measures whether consumers actually engage with the additive panel before any D4 weight enters the headline score formula. D4 does NOT enter the score formula until TASK-179X passes. This is a hard sequencing constraint: TASK-179X go/no-go must complete before any D7 proposal for D4 score weighting is opened. If TASK-179X fails the engagement threshold, D4 remains presentation-only indefinitely. |
| **mechanism** | `detect_additives_d4(ingredient_text)` in `score_engine.py` scans for E-number patterns (E330, E-330, ה-330) and Hebrew name variants per the prototype set, with Hebrew final-letter normalization. Deduplication: same additive matched by both E-number and name → emitted once with `match_source = "both"`. Order: first occurrence in ingredient string. Wired at the result-assembly point, inside `if BARI_GLASSBOX_W2:` guard. |
| **category_scope** | CROSS-CATEGORY, adopted-behind-flag (`BARI_GLASSBOX_W2`, default OFF). W2 pilot corpora: hummus + maadanim. D4 signal is architecture-ready for all categories but only hummus + maadanim carry wired frontend JSONs in W2 (`hummus_frontend_v4.json`, `maadanim_frontend_v2.json`). |
| **label_observability** | Fully label-observable — reads `ingredients_raw` / `ingredient_text` (raw BSIP0 panel). EDPG firewall preserved: no external database value enters the score engine directly; the tier lookup is the in-house prototype set (BSIP0 labels only). |
| **evidence_strength / tier** | Per-additive — tiers range from **Strong** (`functional`: E330 citric acid, E500 baking soda) through **Moderate** (`contested`: E407 carrageenan, E955 sucralose) to **Weak / Insufficient** (`disclosure-gap`, `confirmed-negative` anchors: E320 BHA). Tier assignments are in `additive_prototype_set_v1.md` and are not summarised here — the prototype sheet is the authoritative source. Overall framework evidence strength: **Moderate** (the 6-tier taxonomy is a structured expert synthesis; individual tier assignments carry their own evidence grades). |
| **co_sign** | Nutrition D7 — co-signed (TASK-179Q, 2026-06-04). Product D7 — co-signed (TASK-179Q, 2026-06-04). Both required per scoring-rule governance. |
| **fidelity** | Flag OFF = byte-identical; `d4_additives` key absent from result dict. Flag ON = `d4_additives` array emitted, no other field changed. D4 cannot raise or lower a headline score in W2 (presentation-only invariant). |
| **status** | Adopted-behind-flag (`BARI_GLASSBOX_W2`, default OFF; not live-active; OFF = byte-identical). Score-movement path is demand-gated on TASK-179X. This entry closes the governance compliance gap (EV required before or with engine code; TASK-179S shipped without it; this entry is the retroactive filing). |
| **source** | `01_framework/glass_box/additive_prototype_set_v1.md`; `03_operations/bsip2/proto_v0/src/score_engine.py` (D4 detector + `BARI_GLASSBOX_W2` flag); `03_operations/bsip2/proto_v0/src/constants.py` (`GLASSBOX_W2_ADDITIVES`); `03_operations/bsip2/proto_v0/verify_glassbox_w2_off_identical.py`; six-dimension contract §D4; TASK-179S (implementation); TASK-179Q (prototype set + D7 co-sign); TASK-179X (engagement gate — W3 demand gate for score movement). |
| **rollback_flag** | `BARI_GLASSBOX_W2` (default OFF) — unset → `d4_additives` not emitted; engine byte-identical to pre-W2 baseline. |

---

### EV-043 — D4 Expanded Additive Library Tier Assignments (36 additives; W3 annotate-only)

| Field | Value |
|-------|-------|
| **finding_id** | EV-043 (Glass Box Wave 3, D4 tiering; TASK-181B). Extends EV-041 (the 6-tier model + detector) to the full shelf-present set. EV-042 reserved (unfiled) for D3 de-moralization (TASK-179Z) — not reused here. |
| **task** | TASK-181B (Nutrition tiering); inputs from TASK-181A (`additive_library_expanded_v1.md`, Research evidence sheet) and TASK-179Q (W2 prototype tiers, re-confirmed here). |
| **recorded** | 2026-06-04 |
| **dimension** | D4 — additive evidence (annotate-only). |
| **signal** | Tier assignment for each of the **36 additives** in the expanded D4 library (20 carried forward from the W2 prototype + 16 newly added on the displayed shelf). Each additive maps to exactly one of the EV-041 tiers (`functional` / `likely-neutral` / `dose-dependent` / `contested` / `disclosure-gap` / `confirmed-negative`) with a one-line justification citing the 181A curated evidence. The authoritative 36-row table lives in `01_framework/glass_box/additive_tiered_library_v1.md` — this entry records that the assignments exist, are co-sign-gated, and are annotate-only; the tier table itself is not duplicated here. |
| **tier_model** | The 6-tier + `unclassified` fallback model is **unchanged from EV-041** (frozen). No tier definitions are added, removed, or redefined in W3. EV-043 only assigns the existing tiers to additional additives. |
| **source_of_truth** | `01_framework/glass_box/additive_tiered_library_v1.md` (TASK-181B, this entry's deliverable) — the only tier input for W3 Data wiring (TASK-181D). Evidence basis = `01_framework/glass_box/additive_library_expanded_v1.md` (TASK-181A). Prototype tiers in `additive_prototype_set_v1.md` (TASK-179Q) were re-confirmed against the expanded evidence; deltas are documented in the library file §Carried-forward reconciliation. |
| **tier_distribution** | Of 36 additives: **functional 19 · likely-neutral 7 · dose-dependent 5 · contested 3 · disclosure-gap 1 · confirmed-negative 0 · unclassified 1** (E141 copper chlorophylls — see judgment-call resolution). |
| **w3_scope** | **Annotate-only.** Tiers drive **display copy only**. They carry **no headline-grade weight**: no score formula change, no weight, no penalty, no credit. D4 does NOT enter the headline grade in W3. Letting additives move the grade remains a separate, future, owner-gated decision (frozen-invariant tripwire #1). OFF = byte-identical; no published `score`/`grade`/`gate`/`glassBox` field is touched by this entry. No engine code, no JSON edited under TASK-181B. |
| **judgment_calls** | (1) **9 EVIDENCE-GAP additives** (E331/E333/E327/E296/E270/E516/E575, E141, E1412/E1414): tiered on the JECFA "not limited" / FDA CFR anchor where a discrete EFSA numeric opinion is absent — the metabolic-acid salts and modified-starch variants land `functional`; confidence stated as Strong on the JECFA+FDA concordance. (2) **E100 curcumin & E960 steviol** numeric ADIs with documented over-exposure subgroups: the over-exposure is supplement-context (curcumin) / children-as-high-consumers at the sweetener axis (steviol), **not** food-colour/typical-use exposure → curcumin = `functional` with a context note; steviol = `dose-dependent` (EFSA over-exposure flag MODERATE is a genuine use-level signal, consistent with the other NNS in the set). (3) **E141 copper chlorophylls**: US/EU divergence (not FDA-approved for general US food use) is treated as a **D5 disclosure note, not a D4 tier move** (jurisdictional approval status is not an evidence-of-harm signal); the EFSA copper-release caveat + absence of a clean single numerical EFSA ADI means the additive cannot be cleanly tiered on the available anchor → `unclassified` with reason, the one true fallback in the set. |
| **mechanism** | None new. The existing `detect_additives_d4` detector (EV-041) reads the in-house ingredient panel and emits `tier` per matched additive. EV-043 supplies the lookup values for the 16 newly-added additives so Data (TASK-181D) can extend `GLASSBOX_W2_ADDITIVES` (or its W3 successor). No detector logic change is specified or required by this entry. |
| **category_scope** | CROSS-CATEGORY, annotate-only (behind the existing `BARI_GLASSBOX_W2` flag / its W3 successor, default OFF). Displayed-shelf pilot corpora: hummus + maadanim. Bread carried-forward additives (E282/E481/E472e/E300-dough/E466/E211/E320/E575) are tiered but currently have **0 displayed-shelf frequency** (181A §1.3) — tiered once so the detector is complete when a fuller bread JSON is displayed. |
| **label_observability** | Fully label-observable — reads `ingredients_raw` / `ingredient_text` (raw BSIP0 panel). EDPG firewall preserved: the tier lookup is the in-house tiered library (BSIP0 labels only); no external database value (OFF taxonomy, EFSA, JECFA, FDA) enters the score engine directly — external sources only *justified* the tier on this governance artifact, with citations. |
| **evidence_strength / tier** | Per-additive evidence strength is stated in the library file. Summary: `functional`/`likely-neutral` assignments rest on **Strong** regulatory concordance (EFSA + JECFA + FDA agree, no positive harm signal at food-label exposure); `dose-dependent` rests on **Strong-to-Moderate** (a numeric ADI with a documented exposure-approaching-limit or over-exposure-subgroup pathway); `contested` rests on **Moderate** (a credible peer-reviewed mechanistic/clinical signal in genuine disagreement with the regulatory verdict); `disclosure-gap`/`unclassified` are **Insufficient** by construction (the label or the evidence record does not permit a verdict). Overall framework strength **Moderate** (structured expert synthesis; per-additive grades carry their own confidence). |
| **co_sign** | Nutrition D7 — authored + co-signed (TASK-181B, 2026-06-04). **Product D7 — CO-SIGNED (TASK-181C, 2026-06-04).** Scope/maintenance co-sign (annotate-only; DISPLAY only; does NOT authorize D4 grade movement — separate future owner-gated decision, tripwire #1). Product accepts the 36-row tiered set (distribution 19/7/5/3/1/0/1; shelf-present surface guardrail held; 0-on-shelf additives correctly retained) and accepts both load-bearing judgment calls as authored: **E141 → `unclassified`** (label discloses fine ≠ `disclosure-gap`; evidence record lacks a clean EFSA numeric ADI ≠ forced `functional`; US/EU divergence routed to a D5 note, not a D4 tier move) and the **E960 steviol `dose-dependent` vs E100 curcumin `functional`** split (over-exposure on the sweetener shelf-use axis vs the off-axis supplement channel). Sustainability secured by the maintenance protocol `01_framework/glass_box/additive_library_maintenance_protocol_v1.md` (annual re-verify + quarterly scan + 6 trigger events + Command-Center staleness alerting + a Product go/no-go gate with a FREEZE outcome and a demand-revisit checkpoint carrying the bypassed TASK-179X gate debt). Both co-signs required per scoring-rule governance; both now recorded. TASK-181B closeable; TASK-181D (Data wiring) unblocked. |
| **fidelity** | Flag OFF = byte-identical; no `tier` values emitted. Flag ON = the existing `d4_additives` array is populated for 16 additional additives; no other field changes. D4 cannot raise or lower a headline score in W3 (annotate-only invariant inherited from EV-041 w2_scope and TASK-181 hard boundary). Frozen invariants untouched: milk run_005_headpin, snack 70/B, bread provenance. |
| **status** | Proposed-behind-flag (`BARI_GLASSBOX_W2` / W3 successor, default OFF; OFF = byte-identical). **Both D7 co-signs complete (Nutrition TASK-181B + Product TASK-181C, 2026-06-04).** Not live-active (annotate-only). |
| **source** | `01_framework/glass_box/additive_tiered_library_v1.md` (TASK-181B tier table + justifications + reconciliation); `01_framework/glass_box/additive_library_expanded_v1.md` (TASK-181A evidence); `01_framework/glass_box/additive_prototype_set_v1.md` (TASK-179Q prototype tiers, re-confirmed); EV-041 (tier model + detector); six-dimension contract §D4; TASK-181 (W3 hard boundary — annotate-only). |
| **rollback_flag** | `BARI_GLASSBOX_W2` (default OFF) — unset → no `tier` values emitted; engine byte-identical. EV-043 adds no new flag. |

---

### EV-042 — D3 De-Moralization: Confidence-Scaled Probabilistic Processing Signal (W4) — REVISED 2026-06-04 (TASK-181J / owner directive)

> **REVISION NOTICE (2026-06-04, TASK-181J — owner directive, Glass Box W4 REWORK).**
> EV-042 is **revised in place** (same id retained — the cleaner governance form here, because
> EV-042 was only ever *proposed-behind-flag*; no engine was built [TASK-181G superseded by
> TASK-181K], no score moved, flag never flipped — so the citation chain in the spec / TASK-181
> umbrella / D5-D6 spec is preserved rather than re-pointed at a new id). The supersession is
> **marked, not silent:** the original single-medium-band reasoning is **preserved verbatim**
> below under "**PRE-REWORK BASELINE (superseded 2026-06-04)**" so the prior rationale is not
> overwritten. The revision adds one binding (`bound_value_set_4` — the material/non-material
> test), revises `bound_value_set_2` (the medium band is split), binds the previously-unbound D6
> non-material deduction and the cap-scaling, and re-words the "less punitive" characterization to
> the honest **pull-to-neutral / confidence-first** framing. **Methodology/governance only — no
> engine code, no score move, no flag flip, no published-data edit.** Data re-implements under
> TASK-181K after Product re-co-signs. **Co-sign on the revision: Nutrition D7 — co-signed
> (TASK-181J, 2026-06-04); Product D7 — PENDING (CC routes Product next).**

| Field | Value |
|-------|-------|
| **finding_id** | EV-042 (Glass Box Wave 4, D3 de-moralization; TASK-179Z spec → TASK-181F finalization → **TASK-181J revision**). EV-042 was reserved (unfiled) at EV-043 time for exactly this D3 entry; it does not collide with EV-043 (D4/W3, distinct dimension and flag). This entry binds the values the spec marked "CONCEPTUAL — requires EV-042 + D7 co-sign," **as revised by the W4 rework (owner directive 2026-06-04): the single medium-certainty band is split into MATERIAL and NON-MATERIAL uncertainty by whether the unknown is material to the processing read.** |
| **task** | TASK-179Z (methodology spec, `d3_demoralization_spec_v1.md`); TASK-181F (original finalization + first Nutrition/Product D7 co-sign); **TASK-181J (this revision + Nutrition D7 re-co-sign; Product D7 re-co-sign PENDING)**. W4 engine **re-implementation** task is **TASK-181K** (supersedes the now-stale TASK-181G build), BLOCKED until Product D7 co-signs this revision. |
| **recorded** | 2026-06-04 (original); **revised 2026-06-04 (TASK-181J)** |
| **dimension** | D3 — processing / formulation signal. |
| **signal** | D3 is reframed from a deterministic NOVA-class→fixed-score lookup to a **confidence-scaled probabilistic population-level signal**. The engine emits, per product, `d3_processing_signal: {nova_class, confidence, uncertainty_materiality, population_correlation, modifier, modifier_note, note_he}` on the professional/internal trace surface (the `uncertainty_materiality` field is **new in the TASK-181J revision**). The D3 dimension score replaces the fixed `NOVA_PROCESSING_SCORES` lookup with a pull-toward-neutral formula scaled by confidence in the NOVA assignment **— but the scaling now depends on whether the uncertainty is *material to the processing read* (`bound_value_set_4`):** material uncertainty may shrink D3 (low-band treatment); **non-material uncertainty does NOT move the D3 score (scale = 1.0) and routes the doubt to D6 confidence only.** NOVA-class amplification of HP penalties (`NOVA_HP_WEIGHTS`) is removed — HP detection signals fire on their direct observational criteria without NOVA scaling. The reframe binds **four** value-sets (below). It does NOT change the NOVA classifier itself, `score_whole_food_integrity`/`NOVA_WFI_SCORES`, `DIMENSION_WEIGHTS` (D3 stays 0.15), or any published score. |
| **bound_value_set_1__confidence_criteria** | Confidence in the NOVA assignment is `high` / `medium` / `low`, derived from **ingredient-evidence quality, not from the NOVA class itself** (the de-circularizing move). **`high`** — all three: (1) ingredient list present (not missing/corrupted); (2) NOVA class unambiguous from ingredient signals — either single-ingredient with no additives (NOVA 1), or additives named with E-codes/specific names (not bare generic terms per D5's G4 detector) with a clear processing pattern; (3) no D5 `severe` disclosure band. **`medium`** — default when neither high nor low applies: list present, some/most additives named, class plausible but not fully verifiable (typical multi-ingredient NOVA 2–3 with partial disclosure). **`low`** — any of: (1) no/empty ingredient list; (2) D5 band `partial` or `severe` with closable gaps that could materially affect NOVA assignment (unnamed stabilisers/preservatives/emulsifiers); (3) class inferred primarily from product-name/category heuristics with no corroborating ingredient evidence. **D5-band dependency:** these criteria read D5's `d5_band` output and therefore require `BARI_GLASSBOX_D5D6` active for the full rule. **Two-signal fallback** (when `BARI_GLASSBOX_D5D6` is OFF): confidence is set from ingredient-list present/absent + the NOVA classifier's own confidence band only (criteria (2)/(3) referencing D5 are not evaluated). `BARI_GLASSBOX_W4` subsumes the D5 integration. |
| **bound_value_set_2__confidence_scale** *(REVISED 2026-06-04, TASK-181J)* | `confidence_scale` is now selected by **confidence band AND uncertainty materiality** (`bound_value_set_4`): **high = 1.0** (unchanged) · **low = 0.40** (unchanged) · **medium-MATERIAL = 0.70** (the medium scale-down, applied ONLY when the gap is material) · **medium-NON-MATERIAL = 1.00 (NO score move).** Modifier formula (pull-toward-neutral, unchanged in form): `modifier_score = 50 + (base_score − 50) × confidence_scale`, where `base_score = NOVA_PROCESSING_SCORES[nova_class]` (95 / 85 / 65 / 35, retained as anchors; `neutral = 50.0`). Worked: NOVA 4 high → `35.0` (identical to today); NOVA 4 **medium-material** → `39.5`; NOVA 4 **medium-non-material** → `35.0` (**identical to today — the score does not move; the doubt goes to D6**); NOVA 4 low → `44.0`; NOVA 1 high → `95.0`; NOVA 1 **medium-material** → `81.5`; NOVA 1 **medium-non-material** → `95.0` (no move); NOVA 1 low → `68.0`. The scaling pulls uncertain assignments **toward neutral 50, never toward a worse score**; and **a non-material gap does not move D3 at all** — *unknown reduces confidence first, not quality first* (the governing principle). **Cap-scaling (now BOUND, not deferred):** the PROCESSING_LOAD caps (`NOVA_PROXY_4_ULTRA_PROCESSED` 68, `NOVA_PROXY_3_PROCESSED` 87) are relaxed *toward 100 (no-cap)* by the **same `confidence_scale`** used for the score, i.e. `cap_effective = 100 − (100 − base_cap) × confidence_scale`. Worked for the NOVA-4 cap (base 68): high → `100−(100−68)×1.0 = 68` (today's cap); medium-material → `100−32×0.70 = 77.6`; medium-non-material → `68` (**cap unchanged — a non-material gap does not loosen the ceiling either**); low → `100−32×0.40 = 87.2`. Same form for the NOVA-3 cap (base 87). This binds what the original entry left as "a W4 implementation derivation" — it is now the explicit formula above, consistent with the score-scaling rule and with the non-material = no-move principle (material gaps loosen both score and cap toward neutral; non-material gaps loosen neither). |
| **bound_value_set_3__population_correlation** | Fixed class-level calibration **anchors** (reference field in the trace; NOT a per-product measurement and NOT a multiplier in the score arithmetic): **NOVA 1 = 0.05 · NOVA 2 = 0.15 · NOVA 3 = 0.40 · NOVA 4 = 0.75** (range 0.0–1.0; 1.0 = strong association). Rationale: NOVA 1 ≈ reference/null group; NOVA 2 small positive signal (culinary-processed staples); NOVA 3 = 0.40 is a **central** estimate over a genuinely heterogeneous group (artisan bread → industrial preserves) — read as a central anchor, not a tight value; NOVA 4 = 0.75 is the strong tail that drives the NOVA epidemiology, still a population correlate not a per-product verdict. |
| **bound_value_set_4__uncertainty_materiality** *(NEW — TASK-181J)* | **The material vs non-material test.** Applies **only to the `medium` confidence band** (`high` already scales 1.0 with no doubt to route; `low` already takes the 0.40 shrink regardless — see "low-band note" below). For a medium-confidence product, classify the unresolved/unknown signal as **MATERIAL** or **NON-MATERIAL** using observable inputs already computed by the engine: <br>**`uncertainty_materiality = "material"` if ANY of:** (M1) the NOVA-deciding additive is a **bare-generic** additive term (D5 G4 detector hit — e.g. unnamed "מייצב"/stabiliser, "חומר משמר"/preservative, "מתחלב"/emulsifier) whose *function class is itself the processed-vs-ultra-processed pivot* — i.e. a NOVA-4 marker additive that is present-but-unnamed; (M2) **D5 band = `severe`** (a severe-opaque panel cannot pin the read); (M3) the **unresolved fraction of the ingredient list is large** — operationalise as: unresolved/unmatched ingredient tokens **> 30%** of the list, OR an unnamed compound ingredient ("תערובת"/"בתוספת...") that could carry NOVA-4 markers; (M4) the **decisive criterion — would resolving the unknown plausibly flip the NOVA class?** If revealing the bare term could move the product across a NOVA boundary (e.g. 3↔4), the gap is material *by definition*. <br>**`uncertainty_materiality = "non_material"` if NONE of M1–M4 fire AND the visible signals already pin the read**, i.e.: the resolved/named portion of the list is **legible and sufficient** to fix the NOVA class on its own (e.g. single-ingredient or a short whole-food list), and the unresolved term is **peripheral** — a non-NOVA-deciding generic (e.g. "תבלינים"/spices, "ארומה טבעית"/natural flavour on an otherwise whole-food list, **one** named stabiliser on a legible short list) where resolving it would **NOT** move the NOVA class. Concretely codeable test for M4: hold the resolved portion's NOVA class fixed; if the *worst-case* identity of the unknown (assume it is a NOVA-4 marker) would still leave the class unchanged given the rest of the list, the gap is **non-material**; if the worst-case identity would flip the class, it is **material**. <br>**Low-band note:** the `low` band is unchanged by this revision (still scale 0.40); materiality only splits the `medium` band, because `low` already encodes either no-panel or a severe/heuristic read where the uncertainty is material by construction. D5-band reads require `BARI_GLASSBOX_D5D6` active; the two-signal fallback (D5D6 OFF) evaluates M1/M3/M4 on the classifier + ingredient string only and omits M2. |
| **bound_value_set_5__d6_routing_non_material** *(NEW — TASK-181J; binds the previously-unbound D6 deduction)* | **Where the non-material doubt now lives.** A medium-confidence, **non-material** product does not move D3; instead it emits a **`d3_nonmaterial_gap`** signal to D6 carrying a **−5 confidence deduction** (applied inside the existing `compute_confidence`/`deduct()` accumulator, gated by the flag; reason string `d3_nonmaterial_gap (peripheral unresolved term; processing read pinned)`). **Magnitude justification (−5):** it is **half** the D5 `partial`-band confidence reduction (−10, d5_d6 spec §2.1) — a non-material gap is a *smaller dent in certainty* than a closable structural disclosure gap, by construction (it cannot move the processing verdict), so it must deduct strictly less than the closable-opacity term while still being non-zero (a real if small reduction in the engine's certainty that it sees the full formulation). It is the only new D3→D6 term for the non-material case; **no double-count** — if the same product already triggers the D5 `partial`/`severe` reduction for the *same* unresolved token, D6 takes the **larger** of the two (max, not sum), never both. **Reconciliation of the prior unbound item:** the original entry's `mechanism` row said a `low_confidence_nova` signal routes to D6 for the *low/insufficient* case but never bound a magnitude; that LOW-band→D6 term is hereby bound at **−10** (equal to the D5 `partial` term — a low-confidence NOVA read is at least as corrosive to certainty as a closable structural gap), again `max`-combined with any D5 term, never summed. So the D3→D6 confidence ladder is: **non-material gap = −5 · low-confidence NOVA = −10**, both flag-gated, both `max`-combined with D5, neither a quality penalty (they act *through* confidence only — the Q2 firewall from the D5/D6 spec is preserved). |
| **evidence_claim** | Population-level epidemiological association (Monteiro et al. 2019; Srour et al. 2020 [BMJ, NutriNet-Santé cohort]; IARC 2020): diets with a higher proportion of NOVA-4 foods are associated, **at the population/dietary-pattern level**, with worse health outcomes (obesity, T2D, CVD, all-cause mortality), with NOVA-1 as the reference group and NOVA 2/3 intermediate. This is a dietary-pattern correlate — the evidence does **not** support (a) that any single NOVA-4 product causes harm, (b) that NOVA class predicts an individual product's nutritional quality, or (c) that NOVA class is assignable with high confidence from a typical Israeli retail label. Evidence strength: **Moderate** — the population-level association is robust across multiple cohorts and geographies; the (rejected) extrapolation to per-product quality verdicts is the governance problem this reframe corrects. |
| **methodology_judgment** | Methodology-owner review — original (TASK-181F) confirmed all three value-sets as drafted; **revised (TASK-181J)** for the medium-band split. (1) `confidence_scale`: high=1.0 and low=0.40 unchanged (low=0.40, not 0.0, preserves a residual lean for a weakly-supported NOVA-4 prior while routing the real uncertainty to D6). **The medium band is now split:** medium-material keeps the 0.70 shrink; **medium-non-material = 1.0 (no score move)** — this is the load-bearing rework. The earlier single medium=0.70 conflated two cases: a gap that could flip the processing class (genuinely should pull D3 toward neutral) and a peripheral gap that cannot (where moving D3 *down* on an otherwise-pinned clean read was a quality penalty masquerading as confidence-scaling). Splitting them honours *unknown-reduces-confidence-first*: a non-material gap is a small dent in certainty (→ D6 −5), not evidence of more processing (→ D3 unchanged). (2) `population_correlation` anchors confirmed faithful to the cited cohorts (monotone ordering, near-null NOVA-1 reference, NOVA-4 strong tail); NOVA 3 = 0.40 read as a heterogeneous-group **central** estimate. (3) Confidence criteria confirmed scientifically sound — keying confidence to ingredient-evidence quality (not the NOVA class) is the required de-circularizing move; D5-band dependency and the two-signal fallback are correctly scoped. (4) **REWORDED "less punitive" → the honest framing.** The original entry described medium/low scaling as "less punitive" (NOVA-4 35→44). That framing is retired as imprecise: the mechanism is **pull-to-neutral, confidence-first** — uncertainty makes D3 *less decisive in either direction* (a low-confidence NOVA-1 also moves 95→68, toward neutral, i.e. *down*), and a non-material gap makes D3 **not move at all**, routing the doubt to D6. "Less punitive" wrongly implied a one-directional leniency; the correct characterization is: **D3 contributes a less extreme signal when the read is uncertain, and contributes no signal change when the unknown is peripheral.** The materiality of the gap — not its direction — decides whether D3 moves. |
| **mechanism** *(REVISED — TASK-181J)* | `score_processing_quality(nova_class, confidence, uncertainty_materiality)` returns `50 + (base_score − 50) × confidence_scale(confidence, uncertainty_materiality)` instead of the fixed `NOVA_PROCESSING_SCORES` lookup. Selection of `confidence_scale`: high→1.0; low→0.40; **medium → 0.70 if `uncertainty_materiality=="material"`, else 1.0 (no move)**, where materiality is computed per `bound_value_set_4` (M1–M4 over the D5 G4 bare-generic detector, D5 band, unresolved-fraction >30%, and the worst-case NOVA-flip test). PROCESSING_LOAD caps relaxed toward 100 by the **same** `confidence_scale` per `cap_effective = 100 − (100 − base_cap) × confidence_scale` (`bound_value_set_2`). When `medium`+`non_material`: D3 score AND cap are unchanged, and the engine emits a `d3_nonmaterial_gap` signal → D6 −5 (`bound_value_set_5`). `NOVA_HP_WEIGHTS` scaling removed (HP signals `HP_FAT_SUGAR_COMBO` / `HP_FAT_SODIUM_COMBO` / `HP_CRUNCH_SWEET_COMBO` fire on direct criteria). `d3_processing_signal` struct (now incl. `uncertainty_materiality`) added to the per-product trace. On insufficient ingredient data D3 does **not** invent a NOVA class — `confidence="low"`, score pulled toward neutral, and a `low_confidence_nova` signal routed to D6 at **−10** (`bound_value_set_5`; `max`-combined with any D5 term, never summed). All behind `BARI_GLASSBOX_W4` (default OFF). Data re-implements under **TASK-181K**. |
| **category_scope** | CROSS-CATEGORY, proposed-behind-flag (`BARI_GLASSBOX_W4`, default OFF). Reframe is architecture-level; no per-category copy is bound by this entry beyond the §3 `note_he` candidates (already Product-co-signed, spec L427–482). |
| **label_observability** | Fully label-observable inputs — the NOVA proxy and confidence both read the in-house BSIP0 ingredient panel and (when `BARI_GLASSBOX_D5D6` is ON) the in-house D5 band. EDPG firewall preserved: `population_correlation` anchors are literature-derived calibration constants recorded on this governance artifact with citations; no external database value enters the score engine directly — the engine reads in-house labels only. |
| **evidence_strength / tier** | Framework: **Moderate** (robust population-level NOVA epidemiology; the de-moralizing reframe is a more honest representation of what the label supports, not a stronger claim). `confidence_scale` and `population_correlation` are governed calibration constants (expert synthesis anchored to the cohort literature), not measured quantities — stated confidence is in the **direction and ordering** (Strong) more than the exact magnitudes (Moderate). |
| **co_sign** *(REVISED — TASK-181J)* | **— ORIGINAL (TASK-181F, 2026-06-04):** Nutrition D7 + Product D7 both co-signed the single-medium-band rule (bound_value_set_1/2/3); that co-sign is preserved in the PRE-REWORK BASELINE below and is **not** the operative co-sign for the revised rule. **— REVISION (TASK-181J, 2026-06-04): Nutrition D7 — CO-SIGNED.** The medium-band split (`bound_value_set_4` material/non-material test), the revised scaling (medium-material 0.70 / **medium-non-material 1.0 = no score move**), the bound D6 routing (`bound_value_set_5`: non-material gap −5, low-confidence-NOVA −10, both `max`-combined with D5), the now-bound cap-scaling formula, and the reworded confidence-first framing are all scientifically defensible and bound as authored. The split is the correct correction: it stops D3 from docking quality for a peripheral unknown that cannot move the processing read — honouring *unknown-reduces-confidence-first*. **Product D7 — CO-SIGNED (TASK-181J, 2026-06-04).** Product accepts the medium-band split as the correction it argued for, on all four required points: **(a)** the material/non-material **observable criteria (M1–M4) are the right line** — M4 (worst-case NOVA-flip: hold the resolved class fixed, assume the unknown is a NOVA-4 marker; non-material iff the class still does not flip) is the correct, codeable definition of "material to the processing read," and the M1 (bare-generic NOVA-deciding additive via the D5 G4 detector) / M2 (D5 severe) / M3 (**>30% unresolved fraction** OR an unnamed compound ingredient) OR-conditions feeding it are defensible; the >30% threshold is neither too tight (a couple of peripheral unknowns on a legible list stay non-material) nor too loose (a mostly-illegible panel correctly becomes material). **(b)** **Medium-non-material = no D3 move, doubt routed to D6 −5** — confirmed to deliver the consumer-surface outcome Product required (a small peripheral unknown surfaces as a confidence dent, never a grade cut): worked examples NOVA-4 medium-non-material → 35.0 and NOVA-1 → 95.0 are identical to today, cap unchanged. This kills the original single-medium-band failure mode of docking quality on a mostly-readable product. **(c)** the **−5 / −10 D6 magnitudes** and the `max`-not-sum no-double-count rule are accepted — −5 correctly sits at half the D5 `partial` −10 (a gap that cannot move the verdict must dent certainty strictly less than a closable structural gap, non-zero), low-confidence-NOVA at −10 anchors to the D5 `partial` term, and both act *through confidence only* (Q2 firewall preserved). **(d)** the **bound cap-scaling** (`cap_effective = 100 − (100 − base_cap) × confidence_scale`, same scale as the score) is accepted as internally consistent — material gaps loosen both score and ceiling toward neutral, non-material gaps loosen neither, so the non-material = no-move principle holds end-to-end. Product also notes the fidelity case is **strictly safer** than the original rule (fewer D3 moves; all three frozen invariants hold or move closer to identical). **Both D7 co-signs now recorded (Nutrition TASK-181J + Product TASK-181J, 2026-06-04); the revised rule is adopted on paper and TASK-181K (Data re-implement) is unblocked.** This co-sign approves the *rule on paper* only; it does NOT authorize the live flag-flip (separate owner go-live decision, tripwire #1; carries the bypassed TASK-179X engagement-gate debt). |
| **fidelity** *(REVISED — TASK-181J)* | Flag OFF = byte-identical to the `BARI_GLASSBOX_W2` baseline — no `d3_processing_signal` emitted, `score_processing_quality` runs the current `NOVA_PROCESSING_SCORES` lookup verbatim, `NOVA_HP_WEIGHTS` scaling unchanged. Flag ON: medium-**material** and low-confidence D3 sub-scores move toward neutral; medium-**non-material** D3 sub-scores **do not move** (the doubt is routed to D6 −5); NOVA-class HP amplification dropped. **Net effect vs the original rule: strictly fewer D3 moves** — every product previously docked by the single medium=0.70 band whose gap is *non-material* now does NOT move on D3 (it moves only on D6 confidence). **Frozen-invariant check (this revision):** the split makes the safety case *stronger*, not weaker, in every direction. (1) **Milk run_005_headpin** — predominantly NOVA 1–2 / high-confidence → scale 1.0 → identical (unchanged from original); any medium-band milk SKU whose only gap is peripheral (e.g. "תרבית"/culture named, one generic term) now also does not move → even closer to identical. No breach. (2) **Snack 70/B** — the B ceiling is enforced by independent sugar/calorie guardrails; D3 (weight 0.15) cannot alone promote a bar to A. Under the revision, material-gap bars still pull toward neutral (35→39.5, directionally upward but capped by the guardrails); non-material-gap bars do not move at all. The ceiling holds, and a *non-moving* non-material product is strictly safer than the original rule. (3) **Bread `real_bread_retail_003_v1`** — low-confidence assignments still pull toward neutral (unchanged); medium-band breads with a *legible whole-grain list + peripheral unknown* now do NOT move on D3 (they moved down under the old single-medium band) — a more honest representation and authoring no new published bread run. **No frozen invariant is breached when ON; the revision reduces, never increases, OFF→ON divergence for non-material products.** Flag OFF at co-sign = nothing moves now. **The live flag-flip remains a separate owner go-live decision (tripwire #1); EV-042 binds the rule, it does not authorize a live grade move.** |
| **status** *(REVISED — TASK-181J)* | Proposed-behind-flag (`BARI_GLASSBOX_W4`, default OFF; OFF = byte-identical; not live-active). **REVISION CO-SIGN COMPLETE: Nutrition D7 — co-signed (TASK-181J, 2026-06-04); Product D7 — CO-SIGNED (TASK-181J, 2026-06-04).** The revised rule (medium-band split: medium-material 0.70 / medium-non-material 1.0 = no D3 move + D6 −5; low-conf-NOVA D6 −10; bound cap-scaling) is **ADOPTED on paper** — both required D7 signatures recorded. It supersedes the original single-medium-band rule (181F), which is now history (no engine was ever built on it; 181G superseded by 181K). **TASK-181K (Data re-implement) is UNBLOCKED.** Live grade movement additionally requires a separate owner go-live decision (tripwire #1; carries the bypassed TASK-179X engagement-gate debt). |
| **source** *(REVISED — TASK-181J)* | TASK-181J (this revision); TASK-181 umbrella "W4 REWORK" section; owner directive 2026-06-04. Prior: `01_framework/glass_box/d3_demoralization_spec_v1.md` (§§2.3 / 2.4 / 2.5 / 3 / 4 / 6 — the §2.3/§2.5 single-medium-band text is the pre-rework basis this entry revises; spec to be reconciled by Data/CC at 181K); `01_framework/glass_box/six_dimension_contract_v1.md` §1.2 + §D3; `01_framework/glass_box/d5_d6_rule_spec_v1.md` §2.1 (D6 −10/−20 band reductions — the anchor for the new −5 non-material / −10 low-conf D3→D6 terms); `research/glass_box/engine_enrichment_frameworks_scoping_v1.md` §3 (NOVA cohort literature basis); `03_operations/bsip2/proto_v0/src/score_engine.py` (`score_processing_quality` L697–699, `NOVA_PROXY_4_ULTRA_PROCESSED` cap L1247, `NOVA_HP_WEIGHTS` scaling L1321–1350); `03_operations/bsip2/proto_v0/src/constants.py` (`NOVA_PROCESSING_SCORES` L50, `NOVA_WFI_SCORES` L51, `NOVA_HP_WEIGHTS` L52, `PROCESSING_CAPS` L103–108); literature: Monteiro et al. 2019; Srour et al. 2020 (BMJ); IARC 2020. |
| **rollback_flag** | `BARI_GLASSBOX_W4` (default OFF) — unset → D3 runs the current `NOVA_PROCESSING_SCORES` lookup verbatim; byte-identical to the `BARI_GLASSBOX_W2` baseline. Rollback = unset the flag; no code revert required. |
| **governing_principle** *(181S pre-flip wording correction, 2026-06-05)* | **Pull-to-neutral in both directions — less confident, not less punitive.** The original "less punitive" characterization (pre-TASK-181J) is retired. The correct principle: when the NOVA assignment is uncertain, D3 becomes less decisive in *either direction* — a low-confidence NOVA-1 also pulls toward neutral (95→68, i.e. *downward*). A non-material gap does not move D3 at all; the doubt is routed exclusively to D6 confidence (−5). The engine does not discount quality for unknown factors that cannot flip the processing class — it reduces certainty. Score neither punished nor discounted: the engine is simply less certain. The materiality of the gap — not its direction — determines whether D3 moves. |

#### EV-042 — PRE-REWORK BASELINE (superseded 2026-06-04 by TASK-181J; preserved, not overwritten)

> The text below is the **original `bound_value_set_2` and the "less punitive" characterization
> as co-signed at TASK-181F (2026-06-04, single medium-certainty band, both Nutrition + Product
> D7).** It is retained verbatim so the prior reasoning is visible and the supersession is marked,
> not silent. It is **NOT the operative rule** — superseded by the revised `bound_value_set_2` +
> the new `bound_value_set_4`/`bound_value_set_5` above (TASK-181J). `bound_value_set_1`
> (confidence criteria) and `bound_value_set_3` (population_correlation) are **unchanged** by the
> rework and remain live as shown in the body above.

- **Original `bound_value_set_2__confidence_scale` (superseded):** `confidence_scale`: **high = 1.0 · medium = 0.70 · low = 0.40.** Modifier formula (pull-toward-neutral): `modifier_score = 50 + (base_score − 50) × confidence_scale`, where `base_score = NOVA_PROCESSING_SCORES[nova_class]` (95 / 85 / 65 / 35, retained as anchors; `neutral = 50.0`). Worked: NOVA 4 high → `50+(35−50)×1.0 = 35.0` (identical to today); NOVA 4 medium → `39.5`; NOVA 4 low → `44.0`; NOVA 1 high → `95.0` (identical to today); NOVA 1 medium → `81.5`; NOVA 1 low → `68.0`. The scaling pulls uncertain assignments **toward neutral 50, never toward a worse score** — uncertainty makes D3 less decisive, not more punitive. PROCESSING_LOAD caps (`NOVA_PROXY_4_ULTRA_PROCESSED` 68, `NOVA_PROXY_3_PROCESSED` 87) follow the same confidence-scaling governing principle; the exact cap formula is a W4 (TASK-181G) implementation derivation, not bound numerically here.
- **Original "less punitive" characterization (superseded, re-worded above):** the original entry characterized a low-confidence NOVA-4 moving 35→44 as "less punitive," and treated the single medium band as a uniform 0.70 scale-down regardless of whether the unknown could move the processing read. This was retired by TASK-181J: the medium band split into material/non-material, and the framing corrected to **pull-to-neutral / confidence-first** (uncertainty makes D3 less decisive in *either* direction; a non-material gap does not move D3 at all). See the revised `methodology_judgment` row (item 4) above.

---

## Section B — Guardrails (Misconceptions That Must NOT Be Modeled)

These 20 misconceptions are explicitly excluded from BSIP2 algorithmic treatment. Modeling any of these as if true would produce systematic scoring errors.

| ID | Misconception | BSIP2 Rule |
|----|--------------|------------|
| G-001 | Thermodynamic equivalence of calories — all calories are metabolically identical | BSIP2 must apply food matrix and satiety adjustments; calorie count alone is never the final score |
| G-002 | Inherent harm of all ultra-processed foods — NOVA 4 is uniformly bad | BSIP2 must use Siga-style differentiation (EV-001); fortified cereals and fermented dairy are not equivalent to confectionery |
| G-003 | Insoluble fiber is non-functional / bulking only | Insoluble grain fiber has metabolic benefits (T2D protection, transit regulation); do not penalise insoluble fiber |
| G-004 | PDCAAS is the definitive protein quality measure | PDCAAS over-estimates quality due to fecal nitrogen contamination; do not rely on PDCAAS-derived protein quality claims |
| G-005 | Natural sugars (honey, agave) are metabolically superior to sucrose | Once fructose/glucose enter the portal vein, metabolic pathways are identical; do not grant natural sugar sources a scoring exemption |
| G-006 | All food emulsifiers are uniformly toxic | BSIP2 must differentiate synthetic surfactants (CMC, P80) from lecithins and prebiotic gums (EV-003, EV-019) |
| G-007 | Organic certification guarantees micronutrient superiority | Organic certification verifies pesticide avoidance, not vitamin/mineral concentration; do not award scoring bonus for organic label alone |
| G-008 | Folic acid is harmful for MTHFR carriers | Clinical evidence shows 400µg/day folic acid raises protective red blood cell folate across all MTHFR genotypes; do not penalise folic acid in BSIP2 |
| G-009 | Liquid and solid calories are equally satiating | Liquid matrices produce substantially lower satiety; this is mechanistically established (EV-008) |
| G-010 | Added isolated fiber dampens glycemic response equivalently to intrinsic plant fiber | Isolated non-viscous fibers (inulin, chicory) do not form the gel barrier needed to slow glucose absorption (EV-006, EV-007) |
| G-011 | All saturated fats carry equivalent cardiovascular risk | Hard cheese calcium saponification (EV-014) and the fat ratio model (EV-012) specifically contradict this |
| G-012 | Non-caloric sweeteners have zero metabolic impact | Sucralose and saccharin can induce dysbiosis-mediated glucose impairment in susceptible individuals (EV-017) |
| G-013 | Industrial heating always degrades nutritional value | HPP and controlled heat increase carotenoid bioaccessibility (EV-003 related); heating is not uniformly harmful |
| G-014 | High protein content equals high protein quality | Limiting amino acids (lysine in wheat) cap the utility of all other amino acids; protein density ≠ quality |
| G-015 | Sodium and potassium should be evaluated in isolation | Na:K ratio is the correct cardiovascular metric (EV-011) |
| G-016 | Allulose and fructose are metabolically equivalent | Allulose is excreted largely unchanged and does not contribute glycemic load (EV-004) |
| G-017 | Raw ingredients are inherently more satiating than processed ones | Processing can concentrate viscous fibers or restructure protein to increase satiety |
| G-018 | Any dietary carrageenan causes colitis | Food-grade undegraded carrageenan at label doses is distinct from degraded poligeenan used in high-dose in vitro studies; do not treat carrageenan as equivalent to poligeenan for consumer messaging |
| G-019 | All fortified minerals are equivalent to intrinsic minerals | Non-haem iron in plant matrices is inhibited by phytate and polyphenols; fortified iron bioavailability is compound-specific (EV-016) |
| G-020 | A single category-free algorithm can fairly score all foods | BSIP2 must apply category-specific calorie density tables, guardrails, and pool rules; universal scoring is constitutionally rejected |

---

## Section C — Do-Not-Model-Yet (High Uncertainty — Deferred)

These 20 domains have insufficient data quality, high individual variability, or require inputs unavailable from packaged food labels. They are deferred from algorithmic treatment.

| ID | Domain | Deferral Reason |
|----|--------|----------------|
| U-001 | Synergistic multi-additive toxicity | Cumulative interactive effects across cocktails of additives have not been characterized in humans |
| U-002 | Individual gut microbiome emulsifier susceptibility | CMC/P80 degradation rate varies by individual microbiome baseline; population-level penalty is justified but individual prediction is not |
| U-003 | Quantitative satiety prediction for mixed meals | Complex multi-signal regulation; mathematical precision without physiological monitoring is not achievable |
| U-004 | Phytochemical bioavailability from commercial matrices | Flavonoid/polyphenol absorption is highly matrix-, co-nutrient-, and microbiota-dependent |
| U-005 | Long-term human cardiometabolic effects of mogrosides | Acute glycemic safety confirmed; long-term cohort data on insulin sensitivity and lipid profiles insufficient |
| U-006 | Dietary AGE absorption kinetics | Proportion absorbed vs endogenously generated under varying metabolic states is debated |
| U-007 | Microbial synthesis of Vitamin K2 from dietary fiber | Colonic menaquinone synthesis rate and systemic absorption not predictable from label data |
| U-008 | Interactive effects of pesticide residues and synthetic emulsifiers | No clinical evaluation; theoretical risk only |
| U-009 | Chronic toxicological limits of 3-MCPD and glycidyl esters | Established for infant formula; adult low-dose chronic impact under high uncertainty |
| U-010 | Predictive modeling of postprandial insulin response from labels | Incretin-modulated insulin response is too individual to model from macronutrients alone |
| U-011 | Subclinical epithelial permeability from occasional additive exposure | Chronic vs occasional exposure distinction not quantitatively established in humans |
| U-012 | Comparative long-term efficacy of synthetic vs food-derived vitamin forms | High statistical confounding between vitamin isomers and synthetic salts in long-term trials |
| U-013 | Comparative satiating capacity of fermentable vs viscous fibers | SCFA-mediated GLP-1 release from fermentable fiber is highly variable between individuals |
| U-014 | Acrylamide variance within product batches | Acrylamide levels fluctuate dramatically within batches; not predictable from ingredient label alone |
| U-015 | Micronutrient bioavailability under varying dietary tannin loads | Inhibition of non-haem iron by coffee/tea tannins is meal-timing and gastric-pH dependent |
| U-016 | Allulose-induced GLP-1 release thresholds in non-diabetic humans | Minimum effective oral dose for GLP-1 stimulation not established |
| U-017 | Systemic accumulation of 4-methylimidazole (4-MEI) | Hepatic enzyme polymorphism variability prevents standardised toxicity calculation |
| U-018 | Glycemic load modifiers in complex re-extruded multi-grain matrices | Starch recrystallisation in re-extruded grains varies dynamically with factory cooling cycles |
| U-019 | Impact of food matrix destruction on peptide hormone translocation | PYY and GLP-1 signalling alteration under matrix destruction is highly individual |
| U-020 | Calcium saponification efficiency in varying gastric pH | The solid-state saponification rate (EV-014) depends on gastric acid and pancreatic lipase which vary significantly with age and health status |

---

## Section D — Implementation Roadmap

### Implement Now (label-observable, strong evidence, low-to-medium complexity)

| Priority | Finding | Signal | Prerequisite |
|----------|---------|--------|-------------|
| 1 | EV-012 Saturated-to-unsaturated fat ratio | `unsaturated_to_saturated_ratio` | None — computed from existing BSIP1 fields today |
| 2 | EV-003 Emulsifier risk differentiation | `mucus_thinning_emulsifier_load` | Hebrew emulsifier vocabulary dictionary |
| 3 | EV-015 Fermentation bonus | `fermentation_quality_bonus` | BSIP1 fermentation markers already extracted |
| 4 | EV-008 Liquid vs solid matrix satiety | `matrix_state_factor` | Archetype routing already available |
| 5 | EV-019 Prebiotic gum exemption | `prebiotic_gum_exemption` | Hebrew gum vocabulary (trivial) |
| 6 | EV-004 Allulose handling | `allulose_adjusted_sugar_g` | Allulose ingredient term detection |
| 7 | EV-005 Polyol laxative threshold | `polyol_laxative_potential` | Polyol ingredient vocabulary |
| 8 | EV-018 Reconstituted matrix flag | `reconstituted_matrix_flag` | Simple text match — trivial |
| 9 | EV-010 Extrusion matrix penalty | `extrusion_matrix_penalty` | Extruded product name/ingredient signals |
| 10 | EV-011 Na:K ratio | `na_k_ratio` | Potassium field must exist; low coverage currently |

### Implement After Prerequisite Work

| Priority | Finding | Signal | Prerequisite |
|----------|---------|--------|-------------|
| 11 | EV-001 Siga/MUP classification | `siga_processing_intensity` | MUP taxonomy dictionary (significant build) |
| 12 | EV-002 At-risk additive count | `at_risk_additive_count` | At-risk additive reference list (maintenance obligation) |
| 13 | EV-006 Viscous fiber | `viscosity_fiber_ratio` | Viscous fiber vocabulary dictionary |
| 14 | EV-007 Intrinsic vs isolated fiber | `fiber_source_quality` | Isolated fiber ingredient term list |
| 15 | EV-009 Intact grain integrity | `grain_matrix_integrity_score` | Grain processing state classifier |
| 16 | EV-014 Hard cheese matrix | `matrix_saponification_index` | Hard cheese sub-pool routing + calcium data |
| 17 | EV-016 Fortification discount | `fortification_discount_factor` | Synthetic fortification ingredient detector |

### Research Further (evidence strong but quantification gap or label data gap)

| Finding | Signal | Gap |
|---------|--------|-----|
| EV-013 Bliss point synergy | `bliss_point_synergy_score` | Calibration thresholds product-dependent |
| EV-017 Sweetener dysbiosis | `sweetener_microflora_disruption_risk` | High inter-individual variability; implement as flag only |
| EV-020 Resistant starch | `resistant_starch_flag` | RS quantity not label-readable |

### Reject (data not available from retail labels)

| Signal | Reason |
|--------|--------|
| `refined_oil_contaminant_exposure` | 3-MCPD levels require batch laboratory analysis |
| Direct postprandial insulin predictions | Too individual; contradicts BSIP2 population-level model |
| Category-free generic scoring | Constitutionally rejected by Bari governance |

---

## Section E — Evidence Gaps

Formally logged gaps where current data or testing is insufficient to resolve a known question. These are watch-items, not blockers, unless explicitly stated. Entries are append-only.

### EVIDENCE-GAP 4 — HP × WFI Interaction at Full-Scale Corpus

| Field | Value |
|-------|-------|
| **gap_id** | EVIDENCE-GAP 4 |
| **title** | HP × WFI interaction at full-scale corpus |
| **status** | OPEN — watch-item |
| **surfaced** | TASK-181R (Nutrition Agent sign-off, 2026-06-05); also logged in `01_framework/glass_box/glass_box_technical_methodology_v1.md` Appendix A |
| **formally_registered** | 2026-06-05 (TASK-181S pre-flip checklist; per cc_comment on TASK-181R) |
| **description** | The interaction between HP de-amplification (fat+salt `HP_FAT_SODIUM_COMBO` and fat+sugar `HP_FAT_SUGAR_COMBO` combos firing at full penalty weight regardless of NOVA class, following the TASK-181J removal of `NOVA_HP_WEIGHTS` scaling) and the WFI (Whole Food Index) scoring dimension has not been formally tested across all six live categories. Pilot data on hummus and maadanim shows no over-penalization issue, but this has not been validated corpus-wide. The concern: in a whole-food product with a naturally elevated fat + salt profile (e.g. a seed-based spread), both an HP signal and a WFI credit may fire simultaneously; the net effect on the final score has only been spot-checked. |
| **why_not_blocking** | The pilot data shows no over-penalization. HP de-amplification reduces (not increases) the HP penalty relative to the pre-W4 NOVA-scaled baseline. WFI credit is independent and additive; the two signals do not create a structural feedback loop — they act on separate score dimensions. No case has been identified where both fire in a way that produces an implausible final score. |
| **required_action** | Monitor for over-penalization patterns when new categories go live. Formal validation required when ≥4 categories have WFI-scored products. If any category produces a product where an HP signal and a WFI credit both fire and the final score appears implausible, escalate to Nutrition Agent for a ruling before that category's scores are published. |
| **rule_change_trigger** | Does NOT require any rule change or score freeze before go-live. A rule change would require a new EV entry + D7 co-sign. |
| **dimensions_involved** | D3 (processing / HP detection) × D1 (Whole Food Index / WFI credit) |
| **source** | TASK-181R return block; `01_framework/glass_box/glass_box_technical_methodology_v1.md` §Appendix A; `01_framework/glass_box/d3_demoralization_spec_v1.md` (HP de-amplification rationale) |

---

### EV-044 — NOVA Proxy Quality-Gate: Single-Ingredient Fast-Path Degradation Guard

| Field | Value |
|-------|-------|
| **finding_id** | EV-044 |
| **task** | TASK-140 (cereals greenfield full cycle, QA-CER-W1 resolution) |
| **recorded** | 2026-06-05 |
| **signal** | `nova_1_fast_path_degraded` — a guard condition on the NOVA proxy's single-ingredient early-return path. The path fires `nova_level=1 / nova_confidence=0.90` when `ing_count==1 and additive_count==0`. This is correct for genuine single-ingredient whole foods (plain rolled oats, whole grain flour). It is INCORRECT when the single-entry ingredient list is an artifact of a scraper failure — marketing text, disclaimer copy, or reconstructed fallback text that the BSIP1 enricher stored in the absence of a real ingredient declaration. Three degradation signals gate the fast-path: (a) `ingredient_text_quality in ("missing","corrupted","malformed")`; (b) `"ingredients_list" in missing_fields`; (c) `ingredients_raw_provenance.source == "bsip1_text_fallback"`. When any fires, the product falls through to the main NOVA classifier and receives a confidence penalty of −0.25 (provenance=fallback). |
| **nutrition_ruling** | Shaped baked-flake cereals (Osem פתיתים אפויים כוכבים / טבעות / אורז / קוסקוס) are **NOVA 3**, not NOVA 1. Production pathway: semolina or flour + water + salt/oil → industrial extrusion → shaped bake. Consistent with NOVA Group 3 (processed foods: Group 1/2 ingredients cooked/baked with salt or oil). EV-009 explicitly names "extruded grain shapes" as milling-disrupted grain. EV-010 (`should_affect_score_now: true`) registers extrusion as a matrix-destruction event. A-grade display is **NOT approved** for these products until EV-010 extrusion signal is implemented (D7 co-sign required). |
| **plain_oat_ruling** | Plain whole rolled oats (שיבולת שועל עבה, קוואקר שיבולת שועל, single ingredient, genuine clean scrape) — NOVA 1 confirmed, A-grade (85+) **display approved**. EV-009 lists rolled oats (not instant) as intact grain with preserved starch granule insulation. EV-010 risk-of-misuse note: extrusion penalty must NOT apply to whole-grain puffed forms or rolled oats (mechanical flattening, preserved cell structure). |
| **data_source** | TASK-140 run_cereals_002 QA-CER-W1; BSIP1 product records (bsip1_cereal_60200, 60408, 60576, 60903); EV-009 (intact grain), EV-010 (extrusion matrix destruction); NOVA framework Group 3 definition. |
| **mechanism** | Guard condition added to `nova_proxy.py` single-ingredient early-return path (lines 83–92). Reads `missing_fields`, `ingredients_raw_provenance.source`, and `ingredient_text_quality` from the product dict before allowing fast-path exit. When blocked, confidence_penalties is populated and the product falls through to the main NOVA scorer with a −0.25 confidence deduction for `bsip1_text_fallback` provenance. |
| **generalizability** | Cross-category: any future category where the Shufersal/OFF scraper fails to capture a real ingredient panel (BSIP0 file not found → `bsip1_text_fallback`) will produce `ingredient_text_quality="clean"` with malformed content. The guard prevents false confident NOVA 1 from propagating to those future runs. |
| **category_scope** | CROSS-CATEGORY. Bug fix to existing logic path — no new scoring signal, no new weight, no flag required. Always-on (no rollback flag needed; the change only removes false confidence, never adds it). |
| **evidence_strength** | Strong — EV-009 and EV-010 both classified Strong; NOVA Group 3 definition is unambiguous for this process type. |
| **label_observability** | Fully label-observable. Gate reads BSIP1 data-quality fields (`missing_fields`, `ingredients_raw_provenance.source`, `ingredient_text_quality`) — all populated at BSIP1 enrichment and available on every product dict. |
| **co_sign** | Nutrition Agent ruling — 2026-06-05 (TASK-140 QA-CER-W1 resolution). Product D7 co-sign required only for the EV-010 extrusion_matrix_penalty scoring signal (follow-up scope); this entry covers the quality-gate bug fix only. |
| **follow_up_scope** | EV-010 extrusion_matrix_penalty signal implementation — detects extruded/shaped product names (פתיתים אפויים, כוכבים, טבעות, פצפוצים) in canonical_name_he and applies a structural_quality deduction for refined-grain extrusion. Requires D7 Product co-sign before implementation. Scoped as cereals-pipeline follow-up, not a TASK-140 gate. |
| **should_affect_score_now** | true (bug fix — already applied in nova_proxy.py 2026-06-05) |
| **source** | `nova_proxy.py` (lines 83–104); EV-009 §intact-grain table; EV-010 §risk-of-misuse (whole-grain puffed exemption); NOVA 4-group framework §Group 3 |

---

### EV-046 — Canonical Nutrition Extraction Path: "פחות מ N" / sub-row total-fat overwrite, permanent systemic fix (EV-029 family; 3rd recurrence)

| Field | Value |
|-------|-------|
| **finding_id** | EV-046 |
| **task** | TASK-192 (Data half — canonical fix). Companion: QA half = the permanent BLOCKING guard (COV-### successor to COV-006) + cross-corpus sweep. |
| **recorded** | 2026-06-05 |
| **layer** | Data ingestion / extraction — NOT a scoring rule. No cap/floor/weight/threshold added (no Tension-5 rule-budget cost). Direct successor to EV-029 / EV-026 (Shufersal scrape-hygiene defects). |
| **trigger (3rd recurrence)** | EV-029 "fixed centrally in `_shared/bsip0_nutrition.py`" but the mis-capture RECURRED in `run_cereals_005`. Evidence: retained raw `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json` — `nutrition.fat_raw="פחות מ 0.5"` for **70/113** products; **0/113** had a plausible structured total fat; `saturated_fat_raw` empty on the whole category; 57/66 scored products carried `fat_g=0.5`. True total fat (e.g. 34.2g for barcode 7290106773714, "גרנולה מיקס קראנץ' מלוח") was on the page but never captured. |
| **two distinct root causes** | (1) **Subrow-marker gap (scrape layer).** `_SUBROW_MARKERS` covered `מתוכו` (final-vav) and `מתוכנ` (final-nun) but MISSED `מתוכמ` — the final-mem plural form "מתוכם" Shufersal uses for the FAT and SUGAR "of which" rows. A generic "of-which fat" sub-row that lacked a רווי/טראנס token therefore fell through to the generic `שומן→fat` rule and overwrote total fat. (2) **Duplicated numeric layer (build layer).** Every per-category BSIP1 builder (`02_build_bsip1_*.py`) re-implemented its OWN `_parse_num`/`_parse_sodium`/`_parse_nutrition`: the `"פחות מ N"` token was flattened to N (losing the upper-bound semantics), and NO builder enforced `total_fat >= saturated_fat`, so a mis-capture sailed through to the scored panel. Duplication = drift: a fix in one builder never reached the others — exactly how EV-029 recurred. |
| **mechanism (the canonical fix)** | One tested code path in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`. Scrape layer: `_SUBROW_MARKERS` now covers every final-form of the "of which" stem (`מתוכמ`/`מתוכנ`/`מתוכו` + bare `מתוכ` defensive) so no sub-row can ever populate a parent total field; `classify_nutr_label` unchanged otherwise (specific subtypes still win; sugar "of which" still captured). Build layer (NEW): `parse_value_bound(raw)→(value,is_upper_bound)` parses `"פחות מ N"`/`"<N"`/`"עד N"` as value<N and labels it; `parse_num`/`parse_sodium_mg` are byte-identical replacements for the per-builder copies; `parse_nutrition_numeric(n)` is the ONE builder path — emits the canonical numeric panel AND enforces `fat_g >= fat_saturated_g` (violations surfaced in an `_integrity` key for the QA guard; the panel is never silently repaired). |
| **call sites migrated** | All 7 Shufersal BSIP1 builders now delegate to the shared path: `shufersal_cereals/02_build_bsip1_cereals.py` (first consumer — feeds TASK-190), `shufersal_cheese/02_build_bsip1_cheese.py` + `_cheese_003.py`, `shufersal_yogurt/02_build_bsip1_yogurt.py` + `_yogurt_004.py`, `shufersal_butter/02_build_bsip1_butter.py`, `shufersal_maadanim/02_build_bsip1_maadanim.py` (its alternate field-name fallbacks preserved by normalising into canonical `*_raw` keys before delegation). `multiretailer_cereals/02_build_bsip1_multiretailer.py` inherits automatically (it imports the cereals builder's `_parse_nutrition`). All 6 Shufersal `01_scrape_*.py` already routed through `parse_nutrition_list` and so inherit the subrow-marker fix. The dead `NUTR_LABEL_MAP` in `shufersal_hummus/01_discover_hummus_shufersal.py` (unused, carried the original broken pattern) was retired. |
| **not migrated (by design)** | **yohananof** parsers (`yohananof/parser.py`, `yohananof_milk/04_parse_and_build_bsip1.py`) — different retailer HTML model (label→value pairs, not a `div.nutritionList`), and structurally immune to the trap: they iterate an explicit label list with the specific `חומצות שומן רוויות`/`טראנס` rows BEFORE `שומנים`, with no generic `שומן→fat` catch-all. Forcing them onto the Shufersal `div`-based parser would change behaviour for no benefit; their numeric `"פחות מ"` handling is already correct. Flagged for a future optional consolidation onto the shared `parse_value_bound`. **multiretailer 01_acquire** reads OFF structured `fat_100g` vs `saturated-fat_100g` as separate fields — no sub-row trap possible. |
| **byte-identity guarantee** | For every panel that was already correct, `parse_num`/`parse_sodium_mg`/`parse_nutrition_numeric` return identical floats and NO `_integrity` key — output is byte-identical (proven by `test_parse_num_byte_identical_to_legacy` + `test_clean_panel_no_integrity_key`). No pipeline was re-run and no published score was touched by this entry. Any category re-score is TASK-190's separately-gated, owner-D7 path. |
| **tests** | `03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py` — 12 tests, all PASS. Fixture = the real `run_cereals_005` raw (`cereals_bsip0_raw_20260601T152207.json`). Covers: the `מתוכם` final-mem gap, total-vs-subrow selection, sugar "of which" still captured, `"פחות מ"` bound semantics, legacy byte-identity, the `sat>total` invariant, and three real-corpus regressions (bug signature present; target barcode's bound recoverable; guard flags ≥50 panels). |
| **label_observability** | Observable: the shared guard `nutrition_implausible()` / `composition_nutrition_report()` emits per-product reasons + corpus %; `parse_nutrition_numeric` additionally exposes the `_integrity` list (`sat_gt_total_fat`, `*_is_less_than_bound`). QA Agent's permanent BLOCKING guard (TASK-192 QA half) consumes the same invariants — co-signed so the canonical rule and the guard agree. |
| **activation_scope** | Always-on data-ingestion fix (parser correctness is not toggled, no flag). Does NOT alter any frozen/published score by itself — scores change only on the owning category's next re-scrape + re-score (TASK-190). |
| **rollback** | Git-reversible; no data migration. Reverting restores the `מתוכמ` gap + the per-builder duplication and is strictly worse. |
| **co_sign needed** | QA Agent — confirm the shared invariants (`total≥saturated`; `"פחות מ"` bound; implausible-low-fat-vs-energy bound; sodium >~2,000 mg/100g absurd-value gate) match the permanent BLOCKING guard. Nutrition Agent — confirm the implausible-low-fat-vs-energy numeric bound (currently `fat≤0.5` AND energy exceeds macro-implied energy by ≥50 kcal). |
| **source** | `_shared/bsip0_nutrition.py` (`_SUBROW_MARKERS`, `classify_nutr_label`, `parse_value_bound`, `parse_num`, `parse_sodium_mg`, `parse_nutrition_numeric`); `test_bsip0_nutrition.py`; EV-029 / EV-026 lineage |

---

---

### EV-047 — kcal Plausibility Upper Bound: Archetype-Conditional Raise (700 → 800)

| Field | Value |
|-------|-------|
| **finding_id** | EV-047 |
| **task** | TASK-191 Phase A (butter pre-ship engine fix, Step 2) |
| **recorded** | 2026-06-05 |
| **layer** | Data integrity / consistency check — NOT a scoring rule. No cap/floor/weight/threshold added. |
| **trigger** | Butter products at 82g fat/100g correctly produce 725–745 kcal via Atwater (82 × 9 = 738 kcal). The prior upper bound of 700 kcal triggered a `kcal_plausible=False` flag and a −10 confidence deduction on valid data, misclassifying structurally sound butter panels as data-integrity anomalies. |
| **evidence_rationale** | Atwater energy calculation is the evidence: fat × 9 kcal/g. For 82g fat/100g (representative Shufersal butter): 82 × 9 = 738 kcal. Ghee can reach ~900 kcal (virtually all fat). The 700 bound was miscalibrated for high-fat archetypes. 800 is the correct ceiling for whole_food_fat / cooking_oil products — no non-fat food legitimately produces 800+ kcal/100g, and the robustness-corpus G3 anomaly case (1800 kcal, OCR/serving confusion) remains well outside the new bound. |
| **evidence_strength** | Low — systematic calibration error, not a nutritional evidence question. The Atwater calculation is the full evidence base. |
| **mechanism** | Upper bound constant in `constants.py` raised from 700 to `KCAL_PLAUSIBLE_UPPER = 800`. `signal_extractor.py` consistency check `kcal_plausible` updated to use `KCAL_PLAUSIBLE_LOWER <= kcal <= KCAL_PLAUSIBLE_UPPER`. At signal extraction time the product category (from router) is not yet available, so a single raised global value of 800 is used safely. `score_engine.py` deduction message and `failure_taxonomy.py` error message updated to reflect new bounds. |
| **scope** | Cross-category: raises the ceiling universally, but only high-fat archetypes (whole_food_fat, cooking_oil) have real products above 700 kcal. No currently-live category (milk, yogurt, snack bars, bread, granola, cheese, hummus, maadanim) produces products in the 700–800 kcal band. Zero score drift for all live categories confirmed by regression check. |
| **activation_scope** | Always-on constant change. No flag required — the prior behaviour was incorrect for butter and a no-op correction for all other categories. |
| **rollback** | Git-reversible. Revert lowers ceiling back to 700 and reintroduces the false positive on butter panels. |
| **co_sign** | Nutrition Agent — self-signed (calibration correction, no D7 required; not a new scoring signal). Regression check required before butter batch run (Phase B). |
| **files_changed** | `constants.py` (KCAL_PLAUSIBLE_UPPER, KCAL_PLAUSIBLE_LOWER, KCAL_PLAUSIBLE_UPPER_STANDARD); `signal_extractor.py` (consistency_checks + L4 flag message); `score_engine.py` (deduction message + import); `failure_taxonomy.py` (error message + import) |
| **should_affect_score_now** | true (bug fix — applied 2026-06-05) |

---

### EV-048 — Sat-Fat Cap Endemic Gate for Intact Dairy Fat (whole_food_fat archetype)

| Field | Value |
|-------|-------|
| **finding_id** | EV-048 |
| **task** | TASK-191 Phase A (butter pre-ship engine fix, Step 4) |
| **recorded** | 2026-06-05 |
| **layer** | Scoring guardrail gate — modifies firing condition of an existing cap. No new cap, no new weight. |
| **trigger** | `ISRAELI_RED_LABEL_1_SAT_FAT` (cap = 55) fires on 100% of butter products because butter's sat-fat content (48–70g/100g) structurally guarantees exceeding the Israeli red-label threshold (5g/100g). The cap was designed to penalise products that could have been reformulated to lower sat-fat. Butter cannot be. Applying it universally to a product class where sat-fat content is compositionally invariant produces no consumer signal: every butter product hits the same cap regardless of quality differentiation. |
| **evidence_rationale** | Dairy fat composition: plain butter = 50–70g saturated fat per 100g total fat (fraction 0.58–0.70). This is a compositional constant of dairy fat, not a formulation choice. The red-label threshold (5g/100g) was designed to identify products with elevated sat-fat relative to what reformulation could achieve. Butter's sat-fat cannot be reduced by the manufacturer — it is the fat. The Israeli Ministry of Health red-label system does not exempt butter, but that is a regulatory transparency requirement; the BSIP2 scoring cap is a separate scoring decision that need not replicate the regulatory boundary verbatim when it produces zero signal differentiation. The regulatory disclosure is retained. |
| **evidence_strength** | Moderate — the composition threshold (sat_frac ≥ 0.50 identifies dairy fat) is sound and defensible for the whole Israeli butter shelf. Not formally calibrated against the full Israeli butter shelf — that calibration is what butter_run_002 will provide. |
| **gate_condition** | Cap is suppressed when: `category == "whole_food_fat"` AND `fat_saturated_g / fat_g >= 0.50`. The sat-fat fraction threshold (0.50) distinguishes plain dairy fat (butter = 0.58–0.70) from: (a) palm-oil-laden spreadable fats with lower fractions; (b) seed-oil-diluted margarines; (c) products with emulsifiers routed to NOVA 3/4 that may not qualify for the WFF floor and are scored lower through that pathway. Any product below the 0.50 fraction still fires the cap normally. |
| **regulatory_annotation** | The Israeli red label (sat_fat) remains registered in `regulatory_quality` as a transparency annotation and is still shown to the consumer. Only the scoring cap (guardrail) is gated. |
| **mechanism** | In `score_engine.py` `evaluate_guardrails()`, the `else` branch (RECAL_P0 OFF) now computes `_wff_sat_frac = sat_f / fat` and evaluates `_endemic_wff_gate = (category == "whole_food_fat" and _wff_sat_frac >= SAT_FAT_CAP_ENDEMIC_WFF_FRACTION)`. When the gate fires, the cap is recorded in `caps_considered` with `fired=False` and the EV-048 note; `check_cap` is not called. Constant `SAT_FAT_CAP_ENDEMIC_WFF_FRACTION = 0.50` in `constants.py`. |
| **scope** | whole_food_fat category only. All other live categories (milk, yogurt, snack bars, bread, granola, cheese, hummus, maadanim) are unaffected — none have `category == "whole_food_fat"`. Zero score drift confirmed by regression check. |
| **live_category_protection** | No currently-live category routes to `whole_food_fat`. Butter is the first whole_food_fat category. The gate is therefore inert on all live categories and activates only for butter (and future whole_food_fat categories). |
| **activation_scope** | Always-on gate within the `evaluate_guardrails` RECAL_P0-OFF path. No flag required — the gate is strictly protective and cannot cause a live-category regression. |
| **rollback** | Git-reversible. Revert reactivates the cap universally on whole_food_fat products. |
| **co_sign** | Nutrition Agent — self-signed (gate on an existing cap; no new scoring signal; whole_food_fat category not yet live). Product Agent D7 co-sign required only if the gate is later extended to a different category or if the fraction threshold is changed. |
| **files_changed** | `constants.py` (SAT_FAT_CAP_ENDEMIC_WFF_FRACTION); `score_engine.py` (gate logic in evaluate_guardrails + import) |
| **should_affect_score_now** | true (applied 2026-06-05; activates on first butter batch run) |
| **follow_up** | butter_run_002 calibration will verify the gate fires correctly across the full Israeli butter shelf and confirm no palm/seed-oil-diluted product incorrectly qualifies. |

---

### EV-049 — Graduated Sodium Treatment for Cereal/Granola (BARI_SODIUM_CEREAL)

| Field | Value |
|-------|-------|
| **finding_id** | EV-049 |
| **task** | TASK-189 |
| **recorded** | 2026-06-05 |
| **layer** | Scoring guardrail — new SODIUM_LOAD graduated penalty + category cap + MoH boundary correction. Scoped to `snack_bar_granola` + `cereal` only. |
| **trigger** | TASK-189 independence analysis on run_cereals_006 (63 products, clean data post TASK-190): 18 products have sodium ≥ 300 mg/100g; only 5 of these are already caught by `HP_FAT_SODIUM_COMBO` (which requires fat ≥ 25% of kcal). The remaining 13 high-sodium products (sodium 300–600 mg/100g, fat ≤ 21% kcal — typical low-fat cereals and cornflakes) receive zero sodium penalty under the base engine. The 700 mg threshold (`HIGH_SODIUM_700MG_PLUS`) is never reached in this category (worst real value = 600 mg). Sodium in the 300–600 mg band is therefore a genuine independent driver that the existing engine does not address. |
| **independence_verdict** | YES — sodium is an independent scoring driver for cereal/granola. 13/18 high-sodium products escape HP_FAT_SODIUM because they are low-fat products where fat_pct < 25%. The graduated treatment addresses a real gap that the fat fix (TASK-190) did not close. |
| **signal** | Three components, all scoped to `snack_bar_granola` + `cereal`: (1) **SODIUM_LOAD graduated penalty** (4-band): `<150→0`, `150–299→−2`, `300–449→−5`, `450–599→−8` inside `SODIUM_FAMILY_BUDGET=8`. Rule name `SODIUM_LOAD_CEREAL_GRAD`. (2) **HIGH_SODIUM_CEREAL_500 cap**: sodium ≥ 500 mg/100g → score cap = 75. Applied in addition to the graduated penalty. (3) **MoH red-label boundary fix**: the Israeli MoH red-label threshold for sodium is 600 mg/100g (inclusive). The base `signal_extractor.py` uses `> 600` (strict), missing exactly-600 products. The correction is applied in `score_engine.py` at the `evaluate_guardrails` + pre-dimension-scoring layer for the cereal/granola scope. |
| **bound_values** | Band thresholds (mg/100g) and penalty magnitudes are calibrated to the clean run_cereals_006 corpus: salted granola shelf sits at 300–463 mg (median 394 mg for the top-9 salted products); sweet/standard cereals that add nominal seasoning sit at 150–300 mg; clean unsalted granola is typically <100 mg. The −5 penalty for the 300–449 band is the most consequential — it resolves ~1 band for a C-range product. The −8 for 450–599 is reserved for products near-approaching the red-label boundary. Cap at 500 mg provides a hard ceiling that prevents salted products from reaching A or top-B on nutritional dimensions alone. |
| **data_source** | run_cereals_006 (63 products, BSIP1 run_cereals_006 post-TASK-190 data fix, Shufersal, 2026-06-05). Sodium range: 6–600 mg/100g; median 100 mg/100g. Products in 300+ band: 18/63 (17 in 300–449, 1 at 600). |
| **before_after** | BARI_SODIUM_CEREAL=on vs run_006 baseline (63 products): 27 products move score, 5 move grade. Grade distribution: B 10→9, C 19→20, D 29→25, E 5→9. Score median: 48.6→46.0. Notable grade movers: מוזלי 30% פירות (D→E, sodium 350), מוזלי בוטנים/לוז/שקדים (D→E, sodium 400), מוזלי צימוק תפוח וקינמון (D→E, sodium 400), ריבועי דגנים עם קינמון (D→E, sodium 320), קורנפלקס אורגני הרדוף (B→C, sodium 600 via boundary fix). |
| **category_scope** | `snack_bar_granola` + `cereal` ONLY. Frozen baselines (bread, milk, snack bars) are fully isolated — the `SODIUM_CEREAL_CATEGORIES` scope guard in both the guardrail and the dimension scoring pre-block prevents any cross-category movement. Bread's legitimate 400–500 mg/100g range is unaffected. |
| **mechanism** | (A) In `evaluate_guardrails`: a `cereal_sodium_scope` flag (`BARI_SODIUM_CEREAL and category in SODIUM_CEREAL_CATEGORIES`) gates three additions to the SODIUM_LOAD family: the `SODIUM_LOAD_CEREAL_GRAD` penalty, the `HIGH_SODIUM_CEREAL_500` cap, and a boundary-correct `HIGH_SODIUM_700MG_PLUS` fallback for ≥700 mg. (B) In `score_product`, immediately before dimension scoring: if in scope and sodium ≥ 600 and "sodium" not in l3 red_labels, a shallow l3 copy is made and sodium is added to red_labels (affects `score_regulatory_quality`). Both paths are conditional on `BARI_SODIUM_CEREAL=on`; with flag OFF the engine is byte-identical to run_006. |
| **evidence_strength** | Moderate. The 300–600 mg sodium range for cereal/granola is real and independently confirmed from Shufersal shelf data. The penalty magnitudes are calibration choices (not derived from a dose-response model) but are proportionate to the scale of the difference between clean granola (<100 mg) and salted granola (350–463 mg). The band boundaries are label-observable thresholds, not physiological thresholds. |
| **label_observability** | Fully label-observable — reads `sodium_mg` (already captured in BSIP0 panel, category-scope from router). |
| **rule_accumulation** | One new penalty rule (`SODIUM_LOAD_CEREAL_GRAD`), one new cap rule (`HIGH_SODIUM_CEREAL_500`), one boundary fix (not a new rule — a correction to an existing signal), all scoped to cereal/granola. The existing cross-category `HIGH_SODIUM_700MG_PLUS` cap is preserved as a belt-and-suspenders fallback for the ≥700 mg case (unreachable in current corpus but defensible for future products). Net addition: 2 rules, 1 boundary correction. |
| **activation_scope** | Behind `BARI_SODIUM_CEREAL` (default OFF). Flag ON required to move scores. No live category is affected when flag is OFF (byte-identity proof: PASS, 63/63 products). |
| **rollback** | Set `BARI_SODIUM_CEREAL=off` (the default). Engine returns to run_006 byte-identical behavior. Git-reversible. |
| **co_sign** | Nutrition Agent — author and self-sign (D7 authority granted per TASK-189 instructions, owner pre-authorized 2026-06-05). Product Agent D7 co-sign required per scoring governance protocol (pending; TASK-189 must be returned to CC before live score movement). |
| **should_affect_score_now** | false — flag-gated; not deployed to any live category. Requires Product Agent D7 co-sign + CC close-readiness gate before activation. |
| **verdict_authoring_note** | If/when BARI_SODIUM_CEREAL is activated and sodium becomes a genuine grade driver, the granola comparison page verdicts must be re-authored so the catch may cite sodium causally (owner direction: category-relative framing — "a clean granola doesn't add this salt"). Currently the verdicts cite sodium as a displayed fact only. |
| **files_changed** | `constants.py` (SODIUM_CEREAL_CATEGORIES, SODIUM_CEREAL_BANDS, SODIUM_CEREAL_CAP_THRESHOLD, SODIUM_CEREAL_CAP_VALUE, SODIUM_CEREAL_RED_LABEL_BOUNDARY); `score_engine.py` (BARI_SODIUM_CEREAL flag, evaluate_guardrails sodium block, score_product red-label boundary correction); `batch_run_cereals_007_sodium.py`; `batch_run_cereals_007_sodium_off.py`; `run_cereals_007_delta_table.py` |

---

### EV-050 — Natural Dairy Trans Fat Exemption from the Trans Fat Veto

| Field | Value |
|-------|-------|
| **finding_id** | EV-050 |
| **task** | TASK-191 sub-task (butter_run_002 pre-ship; D7 self-authored Nutrition Agent, 2026-06-05) |
| **recorded** | 2026-06-05 |
| **layer** | Scoring guardrail gate — modifies firing condition of the trans fat veto. No new dimension weight, no new cap, no new penalty added. |
| **trigger** | butter_run_002 produced 6 candidate products scoring 0/E because USDA FDC SR Legacy entries for plain butter (fdc_id=173410) report fat_trans_g values of 3.28–3.7 g/100g. The engine's `TRANS_FAT_VETO_THRESHOLD` (>1.0 g/100g) fires `score=0`. The FDC values measure naturally-occurring dairy trans fat (primarily CLA and vaccenic acid), not industrially produced trans fat from partially hydrogenated vegetable oil (PHVO). |
| **scientific_rationale** | Industrial trans fat (PHVO-derived elaidic acid, C18:1 Δ9t) and natural dairy trans fat (CLA, primarily cis-9, trans-11 C18:2; vaccenic acid, C18:1 Δ11t) are structurally and metabolically distinct. Industrial trans fat: formed by partial hydrogenation of vegetable oils; suppresses HDL, raises LDL, increases inflammatory markers; dose-response is linear with no safe threshold per WHO (2018) and EFSA (2019); associated with cardiovascular disease and all-cause mortality even at low doses (2% of energy ≈ 0.5–2 g/day). Natural dairy trans fat: naturally produced by rumen biohydrogenation in ruminant livestock; cis-9, trans-11 CLA (conjugated linoleic acid, "rumenic acid") has a distinct evidence profile — multiple human trials show neutral or modestly protective effects on cardiovascular risk markers at dietary doses; vaccenic acid is the metabolic precursor to CLA via mammalian Δ9-desaturase conversion. The dose-response at typical butter consumption (10–30 g/day → 0.3–1.5 g natural trans fat) is substantially less certain than the industrial dose-response. No epidemiological study has demonstrated harm attributable specifically to natural dairy trans fat at realistic consumption levels; the large PURE study found full-fat dairy intake associated with reduced cardiovascular mortality. **Conclusion: the veto was designed for industrial trans fat. Applying it to natural dairy trans fat is a category error.** |
| **evidence_strength** | Moderate. The structural/metabolic distinction is well-established and not disputed. The dose-response for natural dairy trans fat at realistic consumption is less characterized than industrial trans fat — hence Moderate, not Strong. The conclusion (veto does not apply) follows from the distinction itself, not from a beneficial-effect claim. |
| **gate_condition** | Exempt the trans fat veto when: (a) `category == "whole_food_fat"` AND (b) `has_phvo == False` (no partially-hydrogenated vegetable oil marker in the ingredient text). This gate is compositional + categorical — it does NOT rely on a numeric threshold, because the numeric ranges of industrial and natural dairy trans fat overlap (both can reach 2–5 g/100g). The only reliable discriminator is the ingredient source. |
| **gate_rationale** | `whole_food_fat` routing + absence of PHVO is the correct discriminator because: (1) Butter and other ruminant dairy fats always route to `whole_food_fat`; PHVO-containing margarines and spreads contain partially-hydrogenated markers in their ingredient text. (2) A product that is NOT `whole_food_fat` but has elevated trans fat is likely an engineered spread — keep the veto. (3) A `whole_food_fat` product with PHVO markers is a blended/hardened spread (e.g., margarine), not plain dairy fat — keep the veto. The gate cannot be satisfied by a processed spread, regardless of fat content. |
| **has_phvo signal** | New L3 signal in `signal_extractor.py`. Detects "שומן צמחי מוקשה", "שמן צמחי מוקשה", "מוקשה חלקית", "partially hydrogenated" in the ingredient text. Bare "מוקשה" intentionally excluded to avoid false-firing on "עמילן מוקשה" (modified starch). Signal emitted as `has_phvo: bool` on every product trace. |
| **residual_signal** | When the exemption fires, the elevated trans measurement is NOT discarded. The existing `trans_fat_status = "veto"` or `"high_concern"` classification in L3 remains. The `trans_pen` in `_score_fat_quality_sprint1` fires at its normal magnitude (20 for veto/high_concern status) on the fat_quality dimension. The consumer therefore still sees a real fat-quality cost from elevated dairy trans — it is just not the categorical score=0. This is the correct treatment: natural dairy trans fat at 3–5 g/100g is not nutritionally neutral, but it is not a reason to score the same as a partially-hydrogenated margarine. |
| **affected_categories** | `whole_food_fat` ONLY. No currently-live category routes to `whole_food_fat` (butter is the first). Gate is structurally inert on all live categories (milk, yogurt, snack bars, bread, granola, cheese, hummus, maadanim — none are `whole_food_fat`). Zero score drift on live categories confirmed by regression check. |
| **BSIP2_relevance** | Direct — resolves the 6×0/E butter_run_002 products caused by FDC-reported natural dairy trans fat. |
| **implementation_complexity** | Low — one gate condition added to `evaluate_guardrails` + one new L3 bool signal (`has_phvo`) in `signal_extractor.py`. No new scoring rule, no new weight. |
| **recommended_action** | implemented — Nutrition Agent D7 self-authored, 2026-06-05. Product Agent D7 co-sign required before any live score movement (per scoring governance: D7 requires both Nutrition + Product). |
| **should_affect_score_now** | true — gate is always-on (no env flag required; the gate is strictly protective: it can only PREVENT the veto from firing, never add a new penalty). However, no live category is affected. First impact is butter_run_002 (non-authoritative, pre-ship). |
| **required_input_fields** | `normalized_nutrition_per_100g.fat_trans_g`, `category` (from router), `ingredients_text_he` or `ingredients_list` (for `has_phvo` detection). |
| **label_observability** | Fully label-observable. `has_phvo` reads the ingredient text (already required). `category` is the router output. `fat_trans_g` is a standard panel field. |
| **rule_accumulation** | One new L3 signal (`has_phvo`), one gate condition on an existing veto. Net veto scope is narrower than before (strictly fewer products can receive score=0 from this rule). No new caps, penalties, or weights. |
| **activation_scope** | Always-on gate (no env flag). Inert on all live categories. |
| **rollback** | Remove the `_natural_dairy_trans_exempt` gate block from `evaluate_guardrails` in `score_engine.py` and the `has_phvo` block from `signal_extractor.py`. Git-reversible. No live score artifact affected. |
| **guards_verified** | Regression check PASS (see implementation notes). No score movement on any frozen category corpus. |
| **co_sign** | Nutrition Agent D7 — self-authored (TASK-191 sub-task, 2026-06-05). **Product Agent D7 co-sign required** before butter goes live. |
| **risk_of_misuse** | (1) Applying a false "dairy is safe" claim in consumer copy — the gate is an engine correction, not a health claim. Consumer-facing text must not say natural dairy trans fat is harmless. (2) Extending the gate to non-whole_food_fat categories — the gate is explicitly scoped to `whole_food_fat` only. Processed dairy products that happen to contain elevated trans fat (e.g., full-fat cream cheese routed to `dairy_protein`) do NOT qualify — they are not `whole_food_fat`. (3) Assuming absence of PHVO in the ingredient text confirms absence of industrial trans fat in all cases — the signal is necessary but not sufficient for a full trans fat source audit; it is sufficient for the purpose of preventing a categorical veto misfire on plain dairy fat. |
| **notes** | The 6 affected butter_run_002 products: חמאה צרפתית רכה למריחה (trans=3.7, OFF-sourced), חמאה קרי גולד מלוחה, חמאה אנקור מלוחה, חמאה לורפק מלוחה, חמאה טרה מלוחה, חמאה פיזן ברטון מלוחה (all trans=3.28, USDA FDC SR Legacy fdc_id=173410). Ingredient text confirms plain dairy composition (שמנת מפוסטרת or similar; no PHVO). After the gate, these products score on their nutritional architecture and receive the existing `trans_pen = 20` on the fat_quality dimension (trans_fat_status="veto" is preserved in L3, which triggers the fat-dimension penalty in `_score_fat_quality_sprint1`). |

---

*Bari BSIP2 Evidence Registry v1*  
*Chief Nutrition Officer — 2026-05-30*  
*Source: Engineering Architecture for AI-Driven Food and Supplement Intelligence (78pp)*  
*Next review: After first 3 implement-now signals are deployed to BSIP2*
