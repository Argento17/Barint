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
