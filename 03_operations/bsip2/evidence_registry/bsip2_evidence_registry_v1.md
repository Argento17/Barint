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

*Bari BSIP2 Evidence Registry v1*  
*Chief Nutrition Officer — 2026-05-30*  
*Source: Engineering Architecture for AI-Driven Food and Supplement Intelligence (78pp)*  
*Next review: After first 3 implement-now signals are deployed to BSIP2*
