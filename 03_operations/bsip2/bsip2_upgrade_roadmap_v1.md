# BSIP2 Upgrade Roadmap v1

**Classification:** Internal — Scoring Architecture  
**Version:** 1.0  
**Date:** 2026-05-31  
**Owner:** Chief Nutrition Officer  
**Inputs:** BSIP2 Evidence Registry v1, Hummus BSIP0–BSIP1 QA data, Current BSIP2 score engine  
**Critical rule:** Every change must improve product rankings. Scientific validity alone is insufficient.

---

## Executive Summary

The Evidence Registry contains 20 scientifically valid findings. After evaluating each against the actual product corpus and the score engine's current implementation, only **4 findings** meet all Group A criteria today. 

Three of the five initially proposed "top candidates" are reclassified downward. The reasons are not scientific weakness — they are corpus reality, implementation risk, and distortion risk.

**The ranking quality test applied to each finding:**
> Which specific products would rank differently? Is that change directionally correct? What is the false-positive exposure?

**Key empirical findings from corpus audit:**

| Observation | Implication |
|-------------|-------------|
| 0/106 snack bar products contain CMC, P80, or carrageenan | EV-003's high-risk tier has zero current corpus impact; only the lecithin-exemption half is active |
| 16/32 bread products have fermentation markers; 13 of those are commercial yeast (שמרים), only 5 are sourdough (מחמצת) | EV-015 fermentation bonus would incorrectly reward 13 commercial-yeast products if applied today |
| 46/106 snack bar products have sat fat data; low-fat products (fat <3g) have high sat-fraction ratios that are not meaningful | EV-012 fat ratio model requires a minimum fat-density guard or it severely distorts rankings for diet products |
| All hummus products have fat <2g/100g and no saturated fat data | None of the Group A fat/emulsifier signals affect hummus rankings |

**Summary of group assignments:**

| Group | Count | Findings |
|-------|-------|---------|
| A — Controlled Pilot | 4 | EV-012 (guarded), EV-003+EV-019, EV-004, EV-005 |
| B — Requires Foundation | 9 | EV-001, EV-002, EV-006, EV-007, EV-009, EV-010, EV-014, EV-015, EV-016 |
| C — Research Only | 6 | EV-008, EV-011, EV-013, EV-017, EV-018, EV-020 |
| D — Reject | 0 (EV) | 3 non-EV signals explicitly rejected |

---

## Initial Challenge: Re-Evaluating the Proposed Top 5

The five candidates proposed as Group A in the Evidence Registry are each re-evaluated from first principles.

---

### EV-012 — Fat Ratio Model

**Initial verdict:** Group A, trivially implementable.  
**Revised verdict:** Group A — but requires a fat-density guard before activation.

**The problem revealed by simulation:** The ratio model (unsaturated/saturated) produces severe distortions for low-fat products. A diet snack bar with 1.0g total fat and 0.7g saturated fat has a ratio of 0.43 — it would score 44 on the ratio formula versus 80 on the current absolute formula. But 0.7g of saturated fat in a product is clinically trivial. The ratio metric is only meaningful when fat is a significant caloric contributor.

**Corpus reality:** 46/106 snack bar products have sat fat data. The 5 products with the worst fat ratios (including palm-oil-heavy chocolate bars) are already scoring poorly under the current formula. The primary ranking improvement is for fat-dense products where the current formula is genuinely wrong — notably whole_food_fat products (tahini, nut butters) where high fat is expected and the quality signal is which *type* of fat.

**Decision: Group A with explicit design constraint.** The ratio logic activates only when `fat_g >= 8.0`. Below this threshold, current absolute sat fat scoring is retained.

---

### EV-003 — Emulsifier Risk Differentiation  

**Initial verdict:** Group A, ingredient text match sufficient.  
**Revised verdict:** Group A — but with corrected impact assessment.

**The problem:** The current signal extractor already counts lecithin (`מתחלב|לציטין`) as an additive marker, contributing to the `additive_marker_count` that drives the ADDITIVE_MARKERS caps. CMC and P80 are NOT detected at all. So the current system over-penalizes lecithin but does not penalize CMC/P80.

**Corpus reality:** In the snack bar corpus: 37/106 products contain lecithin; 0/106 contain CMC, P80, or carrageenan. Implementing EV-003 today would: (a) stop penalizing lecithin-containing products unfairly, and (b) add CMC/P80 detection that catches zero current products. The ranking impact is exclusively the lecithin exemption.

This is still a correct change — lecithin-containing products ARE being wrongly penalized. But the editorial claim "BSIP2 now differentiates harmful emulsifiers from safe ones" is only half-true today. The harmful emulsifier population in our corpus is zero.

**Decision: Group A — implement as a corrective to the current false penalty on lecithin. Document the CMC/P80 detection as infrastructure for Wave 2 categories (dairy, spread) where these emulsifiers are more prevalent.**

---

### EV-015 — Fermentation Bonus

**Initial verdict:** Group A, BSIP1 fermentation markers already extracted.  
**Revised verdict:** Group B — detection vocabulary must be fixed before scoring activation.

**The critical problem:** BSIP1 `extracted_fermentation_markers` currently captures `שמרים` (commercial yeast) as a fermentation marker. In the bread corpus: 13/16 products with fermentation markers contain commercial yeast only; 5/16 have genuine sourdough starter (`מחמצת`). Activating a fermentation bonus on the current detection would reward 13 industrial breads that rise with commercial yeast — products that do NOT have the phytate degradation and organic acid benefits of true fermentation.

The BSIP2 governance documentation already flags this as the "sourdough D6 threshold problem." Applying the bonus before fixing the detection vocabulary would make rankings *worse*, not better.

**Prerequisite required:** The fermentation vocabulary must distinguish:
- `מחמצת`, `sourdough starter`, `levain` → genuine long fermentation (bonus eligible)
- `שמרים`, `yeast`, `בצק חמץ` → commercial yeast (bonus NOT eligible)
- `חומצה לקטית`, `חומץ`, `מי לימון` → acidulant additions (NOT fermentation, NOT eligible)

**Decision: Group B — implement detection vocabulary upgrade first, then promote to Group A.**

---

### EV-018 — Reconstituted Matrix Flag

**Initial verdict:** Group A, simple text match.  
**Revised verdict:** Group C — zero corpus impact in current categories.

**The problem:** Reconstituted and powdered dairy ingredients are relevant to dairy products. In the current deployed categories (hummus, snack bars, bread), no products contain reconstituted milk powder as a primary ingredient. In the full snack bar corpus of 106 products, 0 products triggered reconstitution signals.

This finding will become Group A when the dairy (milk, yogurt) categories are active. Implementing it now adds code with no ranking impact for any currently evaluated product.

**Decision: Group C for current scope. Promote to Group A at dairy category launch.**

---

### EV-019 — Prebiotic Gum Exemption

**Initial verdict:** Group A, trivial text exemption.  
**Revised verdict:** Group A — bundled with EV-003, low standalone impact.

**The problem:** Gum arabic is a known prebiotic, but its standalone presence in current product corpora is rare and its contribution to additive_marker_count is typically 1 increment. The ranking impact of removing a single additive count from gum-arabic-containing products is +0 to +5 points, rarely enough to change a grade.

The finding is scientifically correct and low-risk. It belongs in Group A as a bundle with EV-003 — both are emulsifier/additive taxonomy corrections and should be implemented in a single sprint.

**Decision: Group A, bundled with EV-003. Not a standalone priority.**

---

## Section A — Group A: Controlled Pilot

### A1 — EV-012: Fat Ratio Model (fat_g ≥ 8.0 guard)

**Finding:** Replace absolute saturated fat scoring with unsaturated-to-saturated ratio for fat-dense products.  
**Design constraint:** Activate only when `fat_g >= 8.0`. Below threshold, current formula unchanged.  
**Implementation:** One-line conditional in `score_fat_quality()`: compute `ratio = (fat_g - sat_f) / sat_f`; replace the `100 - sat_f * 3.0 - sat_frac * 25` formula with a ratio-graduated score when fat_g ≥ 8.

**Expected impact:**

| Category | Direction | Rationale |
|----------|-----------|-----------|
| whole_food_fat (tahini, nut butters) | ↑ +5 to +15 on fat dimension | Sesame and nut fats are predominantly unsaturated; ratio will be 4–8, strongly rewarded |
| snack_bars (palm oil products, sat_frac > 0.7) | ↓ −5 to −15 on fat dimension | Products with coconut oil/palm oil now correctly penalized |
| snack_bars (oat-based, date bars) | ↑ +3 to +8 | These have low sat fraction; ratio reward was suppressed by current formula |
| dairy_liquid, dairy_protein | Minimal | Dairy fat is complex and often has moderate sat fractions; change is ±5 |
| cereal_system | Minimal to ↑ slight | Most cereals are low-fat; many have oat fat which is unsaturated |
| Categories with fat < 8g (hummus, low-fat bread) | No change | Guard prevents distortion |

**Expected score movement range:** −15 to +15 on the fat dimension for affected products. Absolute score impact (fat dimension weight dependent): ±3 to ±8 overall.

**Expected grade migration (snack bars, estimated):**
- 2–4 palm-oil-heavy products: possible B→C
- 2–3 nut/oat-based products currently at C-border: possible C→B
- Overall: <10% of corpus has a grade change

**Validation approach:**
1. Run before/after scoring on snack bar corpus (106 products). Identify all products where fat_dimension_score changes by >5 points.
2. Manual review: do the products that rise (date bars, oat bars) correctly rank above those that fall (chocolate-covered palm oil bars)?
3. Expert check: do the resulting rankings match a nutritionist's intuition for the 5 highest-scoring and 5 lowest-scoring products?
4. Confirm no product with fat_g < 8 has a score change.

**Risk:**
- Medium. The guard prevents distortion in low-fat products. The remaining risk is that some products with high fat from coconut oil or dairy fat get penalized when their fat profile is complex. Mitigation: monitor grade migrations in dairy categories.

---

### A2 — EV-003 + EV-019: Emulsifier Tier Model

**Finding:** Remove lecithin from the additive penalty count; add CMC/P80/carrageenan as high-risk; reclassify gum arabic as prebiotic (not additive).  
**Implementation:** Modify `ADDITIVE_MARKER_PATTERNS` in `signal_extractor.py`:
- Remove `לציטין|E322` from the emulsifier pattern
- Add a new `high_risk_emulsifier` pattern: `CMC|E466|קרבוקסי מתיל|פוליסורבט 80|E433|polysorbate`
- Add a new `high_risk_stabilizer` pattern targeting P80/carrageenan specifically for elevated penalty
- Remove `גומי ערבי|E414|acacia` from the stabilizer count
  
Update `score_additive_quality()` to weight `high_risk_emulsifier` detections at 2× normal additive count contribution.

**Expected impact:**

| Category | Direction | Rationale |
|----------|-----------|-----------|
| snack_bars with lecithin only | ↑ +2 to +6 | Removes 1 from additive_count; if at the 3-marker cap, raises score from capped 72 to uncapped |
| Products with CMC/P80 (Wave 2 categories: dairy, sauce) | ↓ −5 to −20 | Currently zero in corpus; infrastructure ready for dairy launch |
| snack_bars with gum arabic | ↑ +1 to +3 | Removes gum from stabilizer count |

**Expected scope:** 37/106 snack bar products are affected (lecithin-containing). Typical impact: +2 to +6 points. Products near the ADDITIVE_MARKERS_3_PLUS threshold boundary (exactly at additive_count = 3 with lecithin as one marker) would receive the largest benefit (+5 to +10 if the cap lifts).

**Expected grade migration:** 2–5 products may shift C→B if lecithin removal brings them below the 3-marker cap threshold.

**Validation approach:**
1. Run before/after on snack bar corpus. Identify which products change.
2. For each product that rises: verify it genuinely only has lecithin as an "emulsifier" — no CMC/P80/carrageenan. These products SHOULD rank higher.
3. Confirm zero products in snack bar corpus contain CMC/P80 (expected based on corpus audit).
4. Prepare for the inverse signal when dairy categories launch: verify that CMC-containing dairy products score lower than lecithin-only equivalents.

**Risk:** Low. Removing an incorrect penalty is a correction, not a speculation. The only risk is if our ingredient detection misclassifies a high-risk emulsifier as lecithin — mitigated by adding explicit CMC/P80 detection.

---

### A3 — EV-004: Allulose Caloric and Glycemic Exemption

**Finding:** Allulose contributes 0.4 kcal/g and zero glycemic load. Exclude it from sugar scoring.  
**Implementation:** In `signal_extractor.py`: add allulose detection pattern. In `score_engine.py`: when allulose is detected, note it in the trace but do not add to the sugar load calculation.

**Expected impact:**

| Category | Direction | Rationale |
|----------|-----------|-----------|
| Keto/low-sugar snack bars with allulose | ↑ +3 to +10 on sugar dimension | Allulose incorrectly inflates the sugar penalty |
| All other products | No change | Allulose absent |

**Expected corpus scope:** Estimated <5% of current snack bar corpus. Allulose is rare in the Israeli market; it appears primarily in imported keto-positioned products.

**Expected grade migration:** Minimal in current corpus. Will increase in relevance as keto category matures.

**Validation approach:** Identify all products in corpus with allulose in the ingredient list. Verify their sugar dimension score improves. Confirm non-allulose products are unaffected.

**Risk:** Low. The detection is a simple text match. The score adjustment is conservative (flag + note in trace; no full caloric recalculation since quantity is unknown from label).

---

### A4 — EV-005: Polyol Laxative Threshold

**Finding:** Products with multiple polyols above the 10g threshold should receive a gastrointestinal risk flag that reduces their score.  
**Implementation:** In `signal_extractor.py`: add polyol detection patterns for the 6 main polyols with individual Hebrew terms. In `score_engine.py`: when polyol_count >= 2 OR polyol_count >= 1 AND product is keto-positioned, apply a laxative_risk_flag that deducts −5 to −15 from the final score (graduated by polyol count).

**Expected impact:**

| Category | Direction | Rationale |
|----------|-----------|-----------|
| Keto/sugar-free snack bars with 2+ polyols | ↓ −5 to −15 | These products carry real consumer safety risk not currently captured |
| Single-polyol products | ↓ −3 (flag only) | Minor penalty + trace note |
| All other products | No change | |

**Expected grade migration:** 0–3 products with heavy polyol loading could fall D→E. This is correct — products that carry a mandatory laxative warning in the EU/UK should not receive a high BSIP2 grade.

**Validation approach:**
1. Identify all products in corpus with ≥2 polyol types. Manually verify each.
2. Cross-reference: are any of these products currently receiving B or A grades where the polyol loading makes that grade questionable?
3. Confirm that natural polyol-containing whole foods (dates, prunes — which naturally contain sorbitol at low levels) are not incorrectly flagged. Guard: only flag when polyol is listed as a discrete ingredient, not when sorbitol appears as part of a whole food name.

**Risk:** Low for clear-cut keto products. Medium for edge cases (naturally occurring sorbitol in fruits). Mitigate by limiting the flag to products where polyol is listed as a standalone ingredient, not embedded in fruit ingredients.

---

## Section B — Group B: Requires Foundation Work

These findings are scientifically valid and have real ranking improvement potential. They are deferred because implementing them before completing the prerequisite work would produce worse rankings, not better ones.

---

### B1 — EV-001: Siga/MUP Classification

**Scientific case:** Strong. Binary NOVA 4 collapses fortified whole-grain cereals with synthetic ultra-processed confectionery.  
**Why deferred:** Requires a comprehensive MUP taxonomy dictionary with Hebrew ingredient mappings. The taxonomy must correctly assign 500+ common ingredients to MUP1, MUP2, or At-risk tiers. A partial taxonomy is worse than no taxonomy: it would penalize correctly classified items while missing unclassified ones.  
**Prerequisite:** Build and validate MUP taxonomy for the top 200 ingredients across all current category corpora. Validate against expert nutritionist classification before scoring activation.  
**Estimated foundation effort:** 3–5 sessions.

---

### B2 — EV-002: At-Risk Additive Count

**Scientific case:** Strong. Scaling penalty by additive risk level is correct.  
**Why deferred:** Depends on EV-001 MUP taxonomy. Also requires a maintained at-risk additive reference list that is updated as regulatory assessments change. A frozen list becomes outdated and creates systematic scoring errors over time.  
**Prerequisite:** Complete EV-001 taxonomy. Define a versioning protocol for the at-risk list that links to EFSA publication dates.  
**Estimated foundation effort:** 1–2 sessions after EV-001.

---

### B3 — EV-006: Viscous vs Non-Viscous Fiber

**Scientific case:** Strong. Non-viscous soluble fibers (inulin, chicory root) do not dampen glycemic response; treating them identically to psyllium or beta-glucan overstates the glycemic benefit of inulin-fortified products.  
**Why deferred:** Requires a viscous fiber vocabulary dictionary. The current BSIP1 enrichment does not distinguish fiber types. Applying a blanket "viscous fiber" bonus without the vocabulary would either miss true viscous fibers or incorrectly reward non-viscous ones.  
**Prerequisite:** Build viscous fiber vocabulary in Hebrew. Validate on a 20-product test corpus of known fiber compositions.  
**Estimated foundation effort:** 1–2 sessions.

---

### B4 — EV-007: Intrinsic vs Isolated Fiber

**Scientific case:** Strong. Isolated fiber additions do not replicate whole-food fiber matrix benefits.  
**Why deferred:** Closely related to EV-006. Requires distinguishing isolated fiber additions (inulin, pea fiber, resistant dextrin added to ingredient list) from intrinsic fiber sources (whole wheat, rolled oats, bran). Ambiguous formulations exist.  
**Prerequisite:** Build isolated fiber signal vocabulary. Confirm no false-positive classification of intrinsic fiber sources as isolated. Can be built alongside EV-006 vocabulary.  
**Estimated foundation effort:** 1 session (combined with EV-006).

---

### B5 — EV-009: Intact Grain / Milling Disruption

**Scientific case:** Strong. Intact cell walls physically insulate starch from enzymatic digestion; milling destroys this regardless of "whole grain" marketing claims.  
**Why deferred:** "Whole grain flour" and "whole grain" are different things, but are often conflated on Israeli labels. A grain processing state classifier needs to distinguish: (a) intact/cracked grain → high insulation, (b) whole grain flour → medium (milled but whole grain content), (c) refined flour → no insulation. The current `matrix_integrity` module exists but doesn't classify processing state from ingredient text at this level of granularity.  
**Prerequisite:** Extend `matrix_integrity.py` with a grain-form classifier. Validate on cereal and bread corpora.  
**Estimated foundation effort:** 2 sessions.

---

### B6 — EV-010: Extrusion Matrix Destruction

**Scientific case:** Strong. Extrusion fully gelatinizes starch and destroys matrix integrity.  
**Why deferred:** The risk of double-penalization with the existing matrix_integrity module is real. Current BSIP2 already penalizes high-NOVA products; extrusion typically correlates with NOVA 3–4. Adding a specific extrusion penalty on top of existing penalties requires calibration to ensure the combined effect is proportionate, not punishing.  
**Also:** whole-grain puffed products (air-popped whole grain) should be exempt from this penalty — they are extruded but retain fiber content. The distinction between refined-grain extrusion and whole-grain puffing must be explicit in the vocabulary.  
**Prerequisite:** Audit the delta between current matrix_integrity scores and the expected extrusion penalty. Define exemption rules for whole-grain puffed formats. Ensure no double-counting.  
**Estimated foundation effort:** 2 sessions.

---

### B7 — EV-014: Hard Cheese Matrix Exception

**Scientific case:** Strong. Calcium saponification reduces absorbable saturated fat in hard cheese matrices by ~15%.  
**Why deferred:** Requires confirmed hard cheese sub-pool routing (Yellow Cheese category not yet launched). Also requires calcium content data, which is frequently absent from Israeli dairy labels. The exception must not apply to processed cheese or cream cheese.  
**Prerequisite:** Yellow Cheese category routing implementation. Calcium label coverage improvement. Explicit hard vs. processed cheese pool rule.  
**Estimated foundation effort:** Activate at Yellow Cheese category launch.

---

### B8 — EV-015: Fermentation Bonus

**Scientific case:** Strong for genuine long fermentation (sourdough, tempeh, kefir).  
**Why deferred:** The current `extracted_fermentation_markers` detection includes commercial yeast (`שמרים`). In the bread corpus, 13/16 products with fermentation markers have commercial yeast only. Activating a fermentation bonus today would reward industrial bread that rises with baker's yeast — products that do NOT have the phytate degradation or organic acid benefits of true fermentation.

This is not a minor calibration issue. It is a fundamental vocabulary defect that would make rankings WORSE if activated.

**Prerequisite:** Restructure the fermentation marker vocabulary to produce three distinct outputs:
1. `genuine_fermentation: true/false` — requires `מחמצת`, `sourdough`, `levain`, `בצק חמץ מחמצת`
2. `commercial_yeast: true/false` — `שמרים` without sourdough qualifier
3. `acidulant_addition: true/false` — `חומצה לקטית`, `חומץ` as discrete additives

Only `genuine_fermentation = true` triggers the bonus. This must be validated on at least 30 bread products before scoring activation.  
**Estimated foundation effort:** 1–2 sessions for vocabulary. 1 session for validation.

---

### B9 — EV-016: Fortification Discount

**Scientific case:** Strong. Synthetic fortification does not replicate the bioavailability of intrinsic nutrients.  
**Why deferred:** Implementing a 30% discount on fortified nutrients requires careful design. The same nutrient (e.g., Vitamin D, iron) might be critical in one population context and legitimately added to address a genuine dietary gap. The fortification discount should apply to the *marketing claim* scoring, not reduce the health safety value of fortification. Incorrectly designed, this would penalize iodized salt, fortified infant formula, and other genuinely beneficial additions.  
**Prerequisite:** Define explicit rules: fortification discount applies to BSIP2 nutrient scoring but is disclosed separately, not used as a hard deduction in the overall product grade. Design the disclosure mechanism first.  
**Estimated foundation effort:** 2 sessions including governance review.

---

## Section C — Research Only

These findings remain outside production scoring. The science is sound, but evidence that implementation improves ranking quality is insufficient, the data is unavailable from labels, or the ranking distortion risk is unacceptable without better calibration.

---

### C1 — EV-008: Liquid vs Solid Matrix

**Reason:** The beverage archetype's calorie density table already implements a liquid satiety discount at the structural level — the strict calorie thresholds for beverages (95 score at ≤10 kcal/100ml, dropping to 30 at 70 kcal/100ml) are calibrated precisely because liquids require stricter per-calorie standards. Adding a parallel `matrix_state_factor` would double-count an effect already captured architecturally.  
**Re-evaluate:** If and when protein drink or meal replacement products are evaluated in a non-beverage archetype (e.g., high-protein shakes incorrectly routed to dairy_protein). Until then, the existing implementation is adequate.

---

### C2 — EV-011: Sodium-to-Potassium Ratio

**Reason:** Potassium is not required on Israeli nutrition labels. Current corpus coverage: <10% of products declare potassium. A modifier that cannot be applied to 90%+ of products is not a ranking signal — it is a missing data problem. Implementing a Na:K modifier where potassium is absent and must be treated as unknown would create a two-tier scoring system where the minority with potassium data get systematic adjustments, not because they are better products but because they declared more data.  
**Re-evaluate:** When Israeli regulatory requirements include potassium declaration, or when a data enrichment strategy provides reliable potassium estimates for common product types.

---

### C3 — EV-013: Hyper-Palatability / Bliss Point

**Reason:** The mechanism (concurrent optimisation of sugar, salt, fat, and flavour enhancers to override satiety) is scientifically robust. The ranking application is not. The mathematical "bliss point" threshold is product-specific and proprietary. Without calibrated thresholds, this signal would falsely penalize: dates (naturally sweet, salty, fatty), aged cheese (salt + fat + umami), and artisanal nut butters with added salt. Any implementation before threshold calibration would produce more false positives than true positives.  
**Path to Group B:** Calibrate thresholds on a labeled training corpus of known hyper-palatable vs. non-hyper-palatable products. Requires 50+ product expert review before any scoring activation.

---

### C4 — EV-017: Sweetener-Induced Dysbiosis

**Reason:** Evidence is moderate-to-strong for the mechanism, but population-level scoring is not appropriate because of high inter-individual variability. More critically: penalizing sucralose/saccharin in BSIP2 would lower scores for diet products (diet sodas, zero-sugar snack bars) RELATIVE to their high-sugar counterparts. A diet bar with sucralose could end up ranking BELOW a sugar-loaded bar because of the sweetener penalty — the exact opposite of correct ranking.  
**Appropriate implementation:** Disclosure flag in the explanation layer (not in the score). "Contains sucralose — some research links this to gut microbiome changes in sensitive individuals." This is a consumer information function, not a ranking function.

---

### C5 — EV-018: Reconstituted Matrix Flag

**Reason:** Zero products in the current active category corpora (hummus, snack bars, bread) trigger reconstitution signals. Implementing this now adds code with no ranking impact.  
**Path to Group A:** At dairy category launch (milk, yogurt). The finding is correct and implementable; the timing is wrong.

---

### C6 — EV-020: Resistant Starch Identification

**Reason:** The quantity of resistant starch is not declared on Israeli labels. Detection is possible only for RS-specific ingredients (green banana flour, raw potato starch), not for the more common RS3 (retrograded starch from cooked-cooled starches). Without quantity data, only a binary flag is possible, and the score adjustment would be speculative.  
**Re-evaluate:** When resistant starch quantification becomes available from enriched data sources or when RS-specific ingredients become more common in the corpus.

---

## Section D — Rejected Signals

No EV findings (EV-001 through EV-020) are rejected. All represent scientifically valid observations that either belong in a later group or need infrastructure work.

The following signals from the source document's Part 5 are explicitly rejected from BSIP2 production scoring:

| Signal | Reason |
|--------|--------|
| `refined_oil_contaminant_exposure` (3-MCPD) | Requires batch laboratory analysis; not inferrable from ingredient labels |
| Direct postprandial insulin prediction | Per-individual insulin response cannot be modeled from population-level macronutrient data; implementing this would produce false precision |
| Category-free generic scoring | Constitutionally rejected by Bari Governance v1 and empirically demonstrated to produce worse rankings than category-specific approaches |

---

## Section F — Recommended Implementation Sequence

### Sprint 1 — Pilot (4 weeks)

Run the 4 Group A changes in a parallel scoring environment. Do not deploy to production until validation is complete.

1. **EV-012: Fat ratio model with fat_g ≥ 8.0 guard.** Modify `score_fat_quality()`. Run full snack bar corpus (106 products) and compare before/after. Target: 0 grade changes in products with fat < 8g, directionally correct changes in fat-dense products.

2. **EV-003 + EV-019: Emulsifier taxonomy.** Modify `ADDITIVE_MARKER_PATTERNS`. Remove lecithin from additive count. Add CMC/P80 high-risk detection. Add gum arabic exemption. Run full snack bar + hummus corpus. Target: 37 lecithin-containing snack bar products rise; 0 additional products fall.

3. **EV-004: Allulose flag.** Add detection pattern. Target: correct identification and trace annotation for all allulose-containing products without affecting non-allulose products.

4. **EV-005: Polyol risk scoring.** Add polyol vocabulary. Implement graduated penalty. Target: keto products with ≥2 polyol types receive appropriate flag/deduction; whole-food products with naturally occurring sorbitol are not affected.

**Sprint 1 validation gate:**
- No grade migration in the top 10 products from the Hummus Review Framework (TASK-038) unless directionally justified
- All lecithin-only products score ≥ their pre-change score
- No product with fat < 8g has a fat dimension score change
- Polyol flag fires on keto bars and not on date bars

---

### Sprint 2 — Fermentation Vocabulary Foundation (3 weeks)

Build the fermentation vocabulary restructure that EV-015 requires. This is a prerequisite, not a scoring activation.

1. Refactor `extracted_fermentation_markers` to produce three explicit fields: `genuine_fermentation`, `commercial_yeast`, `acidulant_addition`
2. Validate on full bread corpus (32 products): 5 sourdough products should show `genuine_fermentation: true`; 11 commercial-yeast breads should show `commercial_yeast: true, genuine_fermentation: false`; lactic-acid-added products should show `acidulant_addition: true`
3. Gate: vocabulary validation must achieve >90% precision on manually labeled test set before proceeding

After Sprint 2 validation, EV-015 can be promoted to Group A and implemented in Sprint 3.

---

### Sprint 3 — Fiber Vocabulary Foundation (3 weeks)

Build the fiber type vocabulary that EV-006 and EV-007 require. These two findings should be built together.

1. Viscous fiber vocabulary: 15–20 Hebrew terms for gel-forming fibers (psyllium, oat beta-glucan)
2. Isolated/added fiber vocabulary: 15–20 Hebrew terms for non-viscous isolated fibers (inulin, chicory extract, polydextrose)
3. Intrinsic fiber sources: whole-grain ingredient signals that indicate fiber is from the grain matrix
4. Validate on cereal corpus (45 products): expected distribution is mostly isolated fiber (added inulin) in fortified cereals vs. intrinsic fiber in oat-based products

---

### Sprint 4+ — Wave 2 Foundation Work

After Sprint 1–3 are validated, the following foundations can be built in preparation for Wave 2 category launches:

- EV-001/002 MUP taxonomy (for Yogurt/Milk/Cereal category launches)
- EV-009 grain form classifier (for Cereal category launch)
- EV-010 extrusion penalty calibration (bundled with Cereal category launch)
- EV-014 hard cheese exception (at Yellow Cheese category launch)
- EV-016 fortification disclosure design (before Cereal category launch, where DISTORTION-004 is endemic)

---

## Section G — Validation Framework

### Primary Validation Method: Ranking Quality Audit

For each Sprint 1 change, generate a before/after scoring report on the full available corpus. For each product with a grade change, produce a one-line justification:

> `{product_name}: {old_grade} → {new_grade} because {signal}. Directionally correct: {YES/NO/UNCERTAIN}`

Any grade change marked UNCERTAIN requires manual expert review before production deployment.

### Success Criteria

| Criterion | Target | Failure threshold |
|-----------|--------|------------------|
| False positive grade upgrades (product scores higher without genuine quality improvement) | 0 | >1 |
| False positive grade downgrades (good product penalized incorrectly) | 0 | >1 |
| Products with fat < 8g having fat score change | 0 | >0 |
| Lecithin-only products with score decrease | 0 | >0 |
| Keto bars with ≥2 polyols receiving polyol flag | 100% of detected | <80% |
| Change in top-10 ranking order within each category | Directionally justified | Any unjustified reordering |

### Validation Categories

**Recommended first validation category for Group A pilot:** Snack bars.

Reasons:
- Largest corpus (106 products)
- Highest emulsifier diversity (37/106 have lecithin)
- Highest fat profile diversity (ratio 0.19 to 9.05)
- Clear "obviously correct" benchmarks: date bars and almond bars should rank above palm-oil chocolate wafers

**Second validation category:** Bread (for EV-015 fermentation vocabulary validation in Sprint 2).

**Not recommended for initial validation:** Hummus. The hummus corpus has near-zero fat, no saturated fat data, and no emulsifiers in most products. None of the Group A signals affect hummus rankings. Hummus validation is appropriate for future signals (e.g., whole food integrity, ingredient count, processing level).

### Regression Check Protocol

Before any Group A change enters production, run the existing router regression corpus (12/12 PASS requirement) to confirm no unintended routing changes. Also run the BSIP2 explanation engine validation suite to confirm explanation text does not reference signals that are no longer the primary scoring factor after the change.

---

## Summary Tables

### Group A — Complete

| Finding | Signal | Fat guard? | Corpus impact | Sprint |
|---------|--------|-----------|---------------|--------|
| EV-012 | `unsaturated_to_saturated_ratio` | fat_g ≥ 8.0 | 46 snack bar products | 1 |
| EV-003+EV-019 | `mucus_thinning_emulsifier_load`, `prebiotic_gum_exemption` | None | 37 lecithin products rise | 1 |
| EV-004 | `allulose_adjusted_sugar_g` | None | <5 products currently | 1 |
| EV-005 | `polyol_laxative_potential` | Natural source guard | Keto segment | 1 |

### Group B — Complete

| Finding | Prerequisite | Target sprint |
|---------|-------------|--------------|
| EV-015 | Fermentation vocabulary restructure | 3 (after Sprint 2 vocab) |
| EV-006 | Viscous fiber vocabulary | 4 (after Sprint 3) |
| EV-007 | Isolated fiber vocabulary | 4 (after Sprint 3) |
| EV-001 | MUP taxonomy dictionary | Wave 2 |
| EV-002 | At-risk additive list + maintenance protocol | Wave 2 |
| EV-009 | Grain form classifier | Cereal launch |
| EV-010 | Extrusion penalty calibration + matrix integrity audit | Cereal launch |
| EV-014 | Hard cheese routing + calcium data | Yellow Cheese launch |
| EV-016 | Fortification disclosure design | Cereal launch |

### Group C — Complete

| Finding | Reason summary |
|---------|---------------|
| EV-008 | Already captured by beverage archetype calorie thresholds |
| EV-011 | Potassium data gap; <10% of products declare it |
| EV-013 | Calibration undefined; high false-positive risk for natural foods |
| EV-017 | Inter-individual variability; implement as disclosure flag, not score |
| EV-018 | Zero corpus impact until dairy launch |
| EV-020 | RS quantity unobservable from labels |

---

*BSIP2 Upgrade Roadmap v1*  
*Chief Nutrition Officer — 2026-05-31*  
*Derived from: BSIP2 Evidence Registry v1 + corpus audit (hummus 69 products, snack bars 106 products, cereals 45 products, bread 32 products)*  
*Next review: After Sprint 1 validation gate is passed*
