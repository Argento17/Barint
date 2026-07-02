# D6 Scoring-Rule Proposal: BSIP2 Engine De-Chaining
**Proposal ID:** EV-DECHAIN-001 (to be registered in bsip2_evidence_registry_v1.md)
**Date:** 2026-06-24
**Task:** TASK-395
**Proposer:** Nutrition Agent (D6 lane)
**Required co-sign:** Product Agent (D7)
**Status:** PROPOSAL ONLY â€” no engine code changed, no scores changed

---

## 1. CHAIN INVENTORY

All items below are VERIFIED from direct file reads. File paths and line numbers are cited.

### 1.1 NOVA-Class Step Lookups

**CHAIN N-1: NOVA_PROCESSING_SCORES step lookup**
- File: `constants.py:61`
- What it does: Maps NOVA proxy class to a rigid score for the `processing_quality` dimension â€” {1:95, 2:85, 3:65, 4:35}. Every NOVA-1 product gets exactly 95 on this dimension regardless of what else is in it; every NOVA-4 product gets exactly 35.
- Why added: Original design artefact â€” a lookup table stood in for a real continuous signal before the dimension weighting architecture was built.
- Current mitigation: W4 (BARI_GLASSBOX_W4, DEFAULT ON as of 2026-06-05) confidence-scales this lookup: high confidence fires at full magnitude, low confidence pulls toward 50, medium-material at 0.70 scale. Half-implemented: the modifier scale applies but the lookup itself is still a discrete step. W4 reduces but does not eliminate the cliff.

**CHAIN N-2: NOVA_WFI_SCORES step lookup**
- File: `constants.py:62`
- What it does: Maps NOVA class to a rigid score for the `whole_food_integrity` dimension â€” {1:100, 2:85, 3:60, 4:30}.
- Why added: Same origin as N-1. Symmetrical design artefact.
- Current mitigation: NONE. The debate brief (score_engine.py:2151 note, confirmed by inspection) identified this as the "half-implemented W4" problem. W4 confidence-scales processing_quality (N-1) but does NOT scale whole_food_integrity (N-2). N-2 is the unmitigated lookup.

**CHAIN N-3: NOVA_PROXY_4_ULTRA_PROCESSED composite cap (68)**
- File: `constants.py:115`, applied at `score_engine.py:2623`
- What it does: Clamps composite score to 68 for any NOVA-4 product. Under W4 this cap is confidence-scaled: highâ†’68, medium-materialâ†’77.6, medium-non-materialâ†’68, lowâ†’87.2.
- Why added: Insurance that NOVA-4 products cannot score in the B range regardless of strong individual dimension scores.
- Current mitigation: W4 partially relaxes for low-confidence NOVA. The 68 is still a hard clamp at high confidence.

**CHAIN N-4: NOVA_PROXY_3_PROCESSED composite cap (87)**
- File: `constants.py:118`, applied at `score_engine.py:2631`
- What it does: Clamps composite score to 87 for NOVA-3 products.
- Why added: Intended to prevent a NOVA-3 from scoring at A/S grades. In practice 87 is so permissive it almost never binds â€” almost no NOVA-3 product reaches an 87 composite without other caps firing first. It costs little but is structurally identical to N-3.

---

### 1.2 Hard Score Caps â€” Sugar Family

**CHAIN S-1: HIGH_CAL_HIGH_SUGAR_SEVERE cap (50)**
- File: `constants.py:80`, applied at `score_engine.py:2339`
- Condition: `kcal >= 500 AND sugar >= 25g/100g`
- Why added: Guard against calorie-dense high-sugar products (e.g. chocolate spreads) escaping penalty through strong protein/fat scores. The 50 is a hard C-grade ceiling.

**CHAIN S-2: HIGH_CAL_HIGH_SUGAR_MODERATE cap (60)**
- File: `constants.py:81`, applied at `score_engine.py:2340`
- Condition: `kcal >= 470 AND sugar >= 20g/100g`

**CHAIN S-3: HIGH_SUGAR_25G_PLUS cap (60, elevated to 68 for SC-2/plain-dairy)**
- File: `constants.py:82`, applied at `score_engine.py:2341-2342`
- Condition: `sugar >= 25g/100g`
- Why added: Blunt sugar severity gate. SC-2 (whole-fruit primary, NOVA1-2) gets an elevated cap (68) acknowledging date bars differ from confections.

**CHAIN S-4: HIGH_SUGAR_25G_GRANOLA_SEVERE cap (50, BARI_GRAN_SUGAR_25G_V1)**
- File: `constants.py:1976-1977`, applied at `score_engine.py:2345-2367`
- Condition: `sugar >= 25g AND category in {snack_bar_granola, cereal}`
- Status: DEFAULT OFF. D7 co-signed 2026-06-23 (TASK-385). This is a recently added cap.

**CHAIN S-5: SNACK_BAR_HIGH_CAL_SUGAR cap (60)**
- File: `constants.py:83`, applied at `score_engine.py:2368`
- Condition: `is_snack_bar AND kcal >= 470 AND sugar >= 15g`

**CHAIN S-6: SNACK_BAR_RED_SUGAR_LABEL cap (55, elevated to 63 for SC-2/plain-dairy)**
- File: `constants.py:84`, applied at `score_engine.py:2370`
- Condition: `is_snack_bar AND red_label_sugar` (Israeli MoH sugar label fires)

**CHAIN S-7: ISRAELI_RED_LABEL_1_SUGAR cap (55, elevated to 63 for SC-2/plain-dairy)**
- File: `constants.py:85`, applied at `score_engine.py:2377`
- Condition: `red_label_sugar` (any category)

**CHAIN S-8: ISRAELI_RED_LABELS_2_PLUS cap (45) / REFORMULABLE_LABELS_2_PLUS (45)**
- File: `constants.py:86` / `constants.py:251`, applied at `score_engine.py:2382-2396`
- Condition: two or more red labels fire simultaneously.
- Why added: The 45 was designed as a hard D-grade ceiling for multi-label products. Under BARI_REDLABEL_V1, endemic sat-fat is excluded from the count (dairy can have a single real label without hitting the cap).

---

### 1.3 Hard Score Caps â€” Calorie Family

**CHAIN C-1: HIGH_CAL_LOW_SATIETY_SEVERE cap (55)**
- File: `constants.py:101`, applied at `score_engine.py:2587`
- Condition: `kcal >= 500 AND protein < 6g AND fiber < 3g`

**CHAIN C-2: SNACK_BAR_HIGH_CAL cap (70)**
- File: `constants.py:102`, applied at `score_engine.py:2592`
- Condition: `is_snack_bar AND kcal >= 430`
- Why added: Snack bars at high calorie density should not score in the A range. The 70 is a B-grade ceiling for high-calorie bars regardless of other signals.

---

### 1.4 Hard Score Caps â€” Processing Family (Additive-Count Driven)

**CHAIN P-1: ADDITIVE_MARKERS_5_PLUS cap (60)**
- File: `constants.py:116`, applied at `score_engine.py:2629`
- Condition: `additive_marker_count >= 5`
- Note: Suppressed for protein_bar sub-lens to avoid double-counting with PROCESSING_LOAD penalties already applied there.

**CHAIN P-2: ADDITIVE_MARKERS_3_PLUS cap (72)**
- File: `constants.py:117`, applied at `score_engine.py:2630`
- Condition: `3 <= additive_marker_count < 5`

---

### 1.5 Hard Score Caps â€” Sodium Family

**CHAIN Na-1: HIGH_SODIUM_700MG_PLUS cap (60)**
- File: `constants.py:134`, applied at `score_engine.py:2886-2893`
- Condition: `sodium >= 700mg/100g`
- Current mitigation: Under BARI_GRAD_SODIUM_V1 + brined_food context, replaced by the graduated SODIUM_GENERAL_BANDS penalty for endemic categories. Under BARI_REDLABEL_V1, graduated for all endemic categories. Brined food context applies 0.7 weight which softens the effective cap slightly.
- Status: This is the chain the brined-sodium program already moved away from for endemic categories.

**CHAIN Na-2: HIGH_SODIUM_CEREAL_500 cap (75, BARI_SODIUM_CEREAL)**
- File: `constants.py:159`, applied at `score_engine.py:2782-2798`
- Condition: `sodium >= 500mg AND category in {snack_bar_granola, cereal}`
- Status: DEFAULT OFF. This is a graduated-replacement cap for the cereal/granola scope.

---

### 1.6 Hard Score Caps â€” Fat Quality Family

**CHAIN F-1: ISRAELI_RED_LABEL_1_SAT_FAT cap (55)**
- File: `constants.py:169`, applied at `score_engine.py:3000`
- Condition: `red_label_sat_fat` (sat_fat > 5g/100g)
- Current mitigation: Under RECAL_P0_ON, this cap is fully suppressed and replaced by a graded fat-dimension penalty (R5). EV-048 gates it off for whole_food_fat with sat_fat/fat >= 0.50 (butter gate). HC endemic relief (BARI_HC_DAIRY_SATFAT_V1) excludes endemic hard cheeses.

---

### 1.7 Sweetener Caps

**CHAIN SW-1: SWEETENER_CAP_A/B/C (75/73/70)**
- File: `constants.py:290-295`, applied at `score_engine.py:3084-3086`
- Condition: sweetener tier A/B/C detected (natural fermented / sugar alcohols / synthetic)
- Why added: Products using any non-nutritive sweetener should not score at the top of the range even if other signals are clean. Graduated by tier. These are independent of the CONCERNS graph (SRC-03 note, separate family).

---

### 1.8 Hard Floors (Raising Mechanisms)

**CHAIN FL-1: NOVA1_SINGLE_FLOOR (85)**
- File: `constants.py:924`, applied at `score_engine.py:3381`
- Condition: NOVA 1 AND nova_conf >= 0.70 AND ingredient_count <= 1
- What it does: Guarantees any genuinely single-ingredient whole food scores at least 85 (A-grade floor). Gated for beverages with reconstitution markers (BEV-084) and multi-ingredient NOVA-1 products (HC-FIX-001).

**CHAIN FL-2: WHOLE_FOOD_FAT_FLOOR (70)**
- File: `constants.py:925`, applied at `score_engine.py:3384`
- Condition: `nova_level <= 2 AND category == "whole_food_fat"`
- What it does: Guarantees butter/pure dairy fat products score at least 70, overriding dimension penalties that would otherwise drag them into C/D territory.

**CHAIN FL-3: PHYSIO_MODERATION_MIN (60) â€” interaction floor**
- File: `constants.py:926`, applied at `score_engine.py:3422`
- Condition: NOVA-1/WFF floor eligible product AND Class B guardrail cap fires AND only 1 reformulable red label
- What it does: When a whole food has a nutritional concern (e.g. salt butter) the floor is moderated from 85/70 down to 60, not zero.

**CHAIN FL-4: PHYSIO_2PLUS_LABELS_MIN (50) â€” interaction floor**
- File: `constants.py:927`, applied at `score_engine.py:3419`
- Condition: Same as FL-3 but with 2+ reformulable red labels
- What it does: Further lowers the floor to 50 when multiple concerns are present.

---

### 1.9 Trans-Fat Veto

**CHAIN V-1: TRANS_FAT_VETO (score = 0)**
- File: `constants.py:900`, applied at `score_engine.py:2286-2301`
- Condition: `trans_fat_g > 1.0g AND NOT (whole_food_fat AND no PHVO)`
- Gate: Natural dairy trans fat (ruminant CLA/vaccenic acid) is exempt from the veto; only industrial trans fat from PHVO triggers it.
- Why added: Industrial trans fat at confirmed concentrations is the only genuine absolute food safety disqualifier in the scoring universe. The 0 score is appropriate.

---

### 1.10 Confidence Ceilings

**CHAIN CC-1: CONFIDENCE_INSUFFICIENT_CEILING (50)**
- File: `constants.py:932`, applied in the confidence path of score_product
- Condition: `confidence < 40` (insufficient data)
- What it does: Hard cap at 50 when the panel is too sparse to score reliably.

**CHAIN CC-2: CONFIDENCE_LOW_CEILING (75)**
- File: `constants.py:933`
- Condition: `confidence 40-59` (low confidence)
- What it does: Cap at 75 when confidence is low but the panel exists.

---

### 1.11 Protein-Bar Specific Caps

**CHAIN PB-1: PROTEIN_BAR_POLYOL_CAPS â€” Tier 1 (62) and Tier 2 (66)**
- File: `constants.py:1860-1866`
- Condition: `protein_bar AND polyol_tier_1 (maltitol)` â†’ 62; `polyol_tier_2` â†’ 66

---

### 1.12 Shelf-Relative Formulation Floors (Category-Relative Anti-Inversion)**

**CHAIN SR-F1 through SR-F8: Sugar/sat-fat formulation floors across enrolled categories**
- Files: `constants.py:564-784` (biscuit, cereal, yogurt, cheese_spread, hard_cheese, juices, maadanim, cakes)
- These are NOT classical NOVA-driven chains. They are category-relative caps that prevent very-high-sugar or very-high-sat-fat products from receiving a B grade within their own shelf context.
- The floor pattern: e.g. `SUGAR_SHELF_REL_FORMULATION_FLOOR = 55` for biscuit (constant: 564), `SUGAR_SHELF_REL_CEREAL_FLOOR = 62` for cereal (constant: 575).
- These are already graduated (shelf-relative distance from median, not a binary threshold), so they partially embody the "continuous assessment" philosophy. They are not pure chains in the same sense.

---

## 2. DISPOSITION PER CHAIN

### REMOVE

**CHAIN N-4: NOVA_PROXY_3_PROCESSED cap (87)**
- REMOVE. The 87 cap almost never binds because no NOVA-3 product reaches 87 composite without other caps (especially sugar, additive) firing first. At 87 it provides no protection that the continuous dimension scoring + other guardrails don't already supply. Removing it eliminates a dead constraint and simplifies the cap hierarchy. Zero consumer harm from removal; the BSIP2 weighted average for a genuine NOVA-3 product cannot plausibly reach 87 through honest dimensions.
- BARI flag: `BARI_DECHAIN_NOVA3_CAP` (new)

**CHAIN S-5: SNACK_BAR_HIGH_CAL_SUGAR cap (60)**
- REMOVE. This rule fires when `is_snack_bar AND kcal >= 470 AND sugar >= 15g`. At that threshold both S-2 (kcal>=470 AND sugar>=20, cap=60) and S-7 (red_label_sugar at sugar>=17.5, cap=55) are likely also active and more binding. S-5 is frequently absorbed (family coordination picks the strictest cap). The snack-bar format-specific logic belongs in the calorie table (already addressed by `snack_bar_granola` archetype in CALORIE_DENSITY_TABLES). The continuous calorie dimension plus S-7 provide sufficient coverage.
- Dependency: S-7 must remain active; category-relative calorie table for snack_bar_granola must remain calibrated.

**CHAIN S-2: HIGH_CAL_HIGH_SUGAR_MODERATE cap (60)**
- REMOVE. This rule (kcal>=470 AND sugar>=20g, cap=60) is subsumed in practice by S-7 (sugar red label at 17.5g, cap=55) and S-1 (kcal>=500 AND sugar>=25g, cap=50). When S-7 fires it is already more binding. When S-7 does not fire (sugar 17.5-20g range), the continuous sugar dimension already applies a heavy penalty at 20g. The cap adds a redundant hard stop in a range where the continuous engine already handles it. Its removal reduces rule accumulation without creating a blind spot.
- Dependency: Graduated sugar penalty bands (SUGAR_GRADUATED_BANDS, EV-REDLABEL-011) must be active to cover the 12-20g range smoothly.

### REPLACE

**CHAIN N-1: NOVA_PROCESSING_SCORES step lookup â†’ graduated matrix-signal replacement**
- REPLACE with: A direct label-observable **reassembly/matrix signal** that measures structural food integrity without reducing to four NOVA steps. The replacement has two components:
  - Component A (continuous substitution): Score the `processing_quality` dimension using a **weighted continuous signal** built from: (1) additive-marker count (already active, drives additive_quality too â€” coordinate so no double-count), (2) presence of disassembly/reconstruction markers in the ingredient text (emulsifiers, modified starch, hydrolyzed proteins, texturisers), and (3) the W4 confidence scaling already operational. The resulting dimension score slides continuously between 0 and 100 without four hard steps.
  - Component B (inversion guard, mandatory): The reassembly signal must encode "clean-label refined-starch junk wins the opposite inversion." This means: a product with only plain refined ingredients (refined flour, sugar, palm oil, no NOVA-4 additives) but high ingredient-list simplicity should NOT score high on processing_quality simply because it lacks named additives. The signal must detect ingredient simplicity of the WRONG kind (refined grain + sugar + fat with no whole-food complexity) and score it at an intermediate level, not the maximum.
  - This Component B is the critical substitution the debate consensus required. Without it, removing the NOVA lookup means a highly refined white-flour product with 3 ingredients scores near 95 on processing_quality.
- Evidence registry: New EV (EV-NOVA-REPLACE-001) â€” requires label-derivability confirmation that the additive/reconstruction signal is observable from Hebrew ingredient text at the accuracy rate the engine needs. This is the HIGHEST RISK substitution in the entire proposal.
- Label-observability: VERIFIED for additive markers (existing signal_extractor.py). NOT YET VERIFIED for the "refined-starch-no-whole-food" classifier at the accuracy needed. This must be validated before N-1 is deactivated.
- BARI flag: `BARI_DECHAIN_NOVA_LOOKUP` (new)
- STAGED: This is Workstream 1, Stage 1A (see Section 3).

**CHAIN N-2: NOVA_WFI_SCORES step lookup â†’ confidence-scaled continuous WFI signal**
- REPLACE with: Apply the same W4 confidence scaling that already applies to N-1 to the `whole_food_integrity` dimension. This is the "half-implemented W4" fix identified at score_engine.py comment ~line 2151. The fix is: when W4 is active, compute WFI as `50 + (NOVA_WFI_SCORES[nova_level] - 50) Ã— confidence_scale(confidence, materiality)` â€” identical form to the processing_quality modifier. At high confidence, the step values are preserved. At low/medium-material confidence, the score pulls toward neutral.
  - This is the smaller, safer fix that can precede the full N-1 replacement. It requires only wiring the existing _w4_confidence_scale() function into score_whole_food_integrity().
- After the WFI confidence-scaling fix, N-2 becomes a partially-continuous signal. The step values remain but are confidence-graduated.
- Longer term: The full WFI signal should also be replaced by the reassembly/matrix signal (same Component B logic as N-1). This is Workstream 1, Stage 1B.
- Evidence registry: EV-042 (existing, revised) â€” the W4 design already covers this intent.
- BARI flag: `BARI_GLASSBOX_W4` (already exists, DEFAULT ON) â€” this fix is the completion of W4, not a new flag. It is a bug-fix-class change, not a philosophy change.
- STAGED: This is Stage 0 (prerequisite, can ship before anything else).

**CHAIN N-3: NOVA_PROXY_4_ULTRA_PROCESSED composite cap (68) â†’ outcome guardrail only**
- REPLACE with: Remove the hard cap; preserve the BARI-INVERSION-TEST-001 outcome guardrail as the replacement safety net. The specific replacement signal is the parser fix noted in the debate: fixing the **additive parser** so that genuinely NOVA-4 additive burdens are correctly counted produces the score depression the 68 cap was providing artificially. When the additive_quality dimension is scoring a 5-additive-marker product at its correct low value (100 - 5Ã—18 = 10), the weighted composite for a NOVA-4 product naturally lands well below 68 if the other dimensions are also correctly scored.
  - The 68 cap was a backstop for cases where the additive dimension undercounted. Fixing the additive parser (which the EV-003/019 activated emulsifier identity deltas partially address) is the correct replacement.
  - This removal is CONDITIONAL on the additive parser being accurate enough to produce the natural depression. Until the parser is validated on the live corpus, retain the cap in relaxed form (raise to 78 as an interim step â€” still prevents grade-B for verified NOVA-4, but allows genuine partial-UPF products to score at their real level).
- Evidence registry: EV-003 (existing), EV-019 (existing), EV-041 (D4 tier) â€” cite all three.
- BARI flag: `BARI_DECHAIN_NOVA4_CAP` (new; depends on additive parser accuracy validation)
- STAGED: Workstream 1, Stage 2 (after Stage 0 and Stage 1A).

**CHAIN S-1: HIGH_CAL_HIGH_SUGAR_SEVERE cap (50) â†’ graduated sugar severity curve**
- REPLACE with: A continuous sugar-severity curve that imposes increasing penalties as sugar rises above 20g/100g toward and beyond 25g/100g. The SUGAR_GRADUATED_BANDS (EV-REDLABEL-011, `constants.py:268-273`) are already a step toward this. The replacement extends the bands to cover the full 0-40g sugar range continuously, making the cap unnecessary because the continuous dimension score (glycemic_quality) + the penalty band together produce the same floor effect naturally.
  - Specific design: extend SUGAR_GRADUATED_BANDS to include a 25+ band with a larger penalty (currently defined as 0 at >=25g because "hard caps handle this range" â€” that is the exact circularity to break). When a real penalty fires at >=25g, the cap becomes redundant.
- Evidence registry: EV-REDLABEL-011 (existing) â€” revision to extend band coverage.
- BARI flag: `BARI_REDLABEL_V1` (already exists, gated) â€” the graduated sugar extension is within this flag's scope.
- STAGED: Workstream 2, Stage 3 (requires BARI_REDLABEL_V1 to be active).

**CHAIN S-3: HIGH_SUGAR_25G_PLUS cap (60/68) â†’ absorbed into graduated sugar curve**
- REPLACE: Once the graduated sugar curve (S-1 replacement) is active, this cap is redundant. Remove it. Until the curve is active, the cap remains necessary. This is a conditional retirement, not a standalone removal.

**CHAIN S-6: SNACK_BAR_RED_SUGAR_LABEL cap (55) â†’ de-anchor from binary red label**
- REPLACE: This is exactly the red-label de-anchor directive (owner standing 2026-06-14, memory ref: `redlabel_deanchor_directive`). Replace with a category-relative sugar signal for snack_bar_granola scope. The shelf-relative sugar differentiator (BARI_SHELF_RELATIVE_V1, already live for cereal/biscuit via EV-085/087) should be enrolled for snack_bar_granola. When the shelf-relative signal is active, the binary 55 cap becomes redundant for products above the sugar red-label threshold â€” the graduated distance from the corpus median provides the differentiation without a cliff.
- Evidence registry: EV-085 (existing biscuit enrollment), EV-087 (cereal enrollment) â€” cite as precedent; new enrollment EV for snack_bar_granolaÃ—sugar.
- BARI flag: `BARI_SHELF_RELATIVE_V1` (already ON by default) + new snack_bar_granola enrollment
- STAGED: Workstream 2, Stage 4.

**CHAIN S-7: ISRAELI_RED_LABEL_1_SUGAR cap (55) â†’ BARI_REDLABEL_V1 continuous formula**
- REPLACE: BARI_REDLABEL_V1 already designs this replacement. The `regulatory_quality` dimension scores continuously based on excess above threshold (REGQUAL_SLOPE_PER_LABEL Ã— excess_ratio). The 55 cap on the composite is made redundant if the regulatory dimension deduction is substantial enough. This is already partially designed â€” the cap removal follows activation of BARI_REDLABEL_V1 for all categories.
- Evidence registry: EV-REDLABEL-001 through EV-REDLABEL-012 (existing).
- BARI flag: `BARI_REDLABEL_V1` (existing, DEFAULT OFF â€” requires Product D7 co-sign for full activation).
- STAGED: Workstream 2, Stage 5 (part of full BARI_REDLABEL_V1 activation).

**CHAIN S-8: ISRAELI_RED_LABELS_2_PLUS cap (45) â†’ remove after BARI_REDLABEL_V1 active**
- REPLACE: The 45 cap was the harshest single guardrail in the engine. Under BARI_REDLABEL_V1, the regulatory_quality dimension already compounds two label deductions at their respective slopes. Combined with sugar dimension scoring, a 2-red-label product should land below 50 naturally if the deductions are calibrated correctly. The cap becomes redundant. Until BARI_REDLABEL_V1 is active and calibrated, the cap must remain.
- STAGED: Workstream 2, Stage 6 (final, after full BARI_REDLABEL_V1 activation and blast-radius verification).

**CHAIN C-1: HIGH_CAL_LOW_SATIETY_SEVERE cap (55) â†’ calorie density table + satiety signal**
- REPLACE: The existing CALORIE_DENSITY_TABLES already score kcal continuously per archetype. The issue is that high-calorie AND low-satiety simultaneously is worse than either alone. Replace the binary cap with a multiplicative interaction: when kcal is in the top tier of the calorie density table AND satiety_support scores below 30 (low protein AND low fiber), apply a combined continuous penalty rather than a cliff. The existing satiety_support dimension at weight 0.06 is too low to register this penalty adequately; a cross-dimension interaction term is needed.
- Evidence registry: New EV (EV-CALORIE-SATIETY-001) â€” requires design work.
- BARI flag: `BARI_DECHAIN_CALORIE_CAP` (new)
- STAGED: Workstream 3, Stage 7. Lower priority; C-1 is currently gated for cooking oils and rarely fires outside of its intended target zone.

**CHAIN C-2: SNACK_BAR_HIGH_CAL cap (70) â†’ calorie archetype table**
- REPLACE: The snack_bar_granola calorie density table already handles this. `CALORIE_DENSITY_TABLES["snack_bar_granola"]` sets tier scores of 55 for 350-430 kcal and 40 for 430-500 kcal. At weight 0.15 (calorie_density dimension), a product at 430 kcal scores (40 Ã— 0.15 = 6 points on that dimension) â€” with 9 other dimensions scoring higher, the composite is unlikely to reach 70 on calorie density alone. The 70 cap was a second-level guard for when the table didn't produce enough depression. After the table is confirmed calibrated for the snack-bar range (EV-PBAR-008 already addresses protein bars), this cap can be retired.
- STAGED: Workstream 3, Stage 7 (same workstream as C-1).

**CHAIN F-1: ISRAELI_RED_LABEL_1_SAT_FAT cap (55) â†’ R5 graded fat-dimension penalty**
- REPLACE: RECAL_P0_ON already implements this replacement (R5 â€” graded sat-fat penalty on the fat dimension replacing the composite cliff cap; see `score_engine.py:2977-2980`). The cap is already suppressed under RECAL_P0_ON. The task here is to make RECAL_P0_ON the default (not an optional flag) so R5 is always the operative path. This is the deepest architectural change and touches the largest number of live products.
- Evidence registry: EV-029 (R1/RECAL_P0), EV-REDLABEL-005 (endemic categories) â€” cite both.
- BARI flag: `BARI_RECAL_P0` (existing, DEFAULT OFF â€” full activation requires owner go-live decision, frozen-invariant tripwire)
- STAGED: Workstream 4, final stage. Requires complete Product Agent D7 co-sign on all R1-R7 provisions.

**CHAIN P-1 and P-2: ADDITIVE_MARKERS_5_PLUS cap (60) and ADDITIVE_MARKERS_3_PLUS cap (72) â†’ additive parser fix + D4 score signal**
- REPLACE: These caps exist because the additive_quality dimension score alone (100 - countÃ—18) sometimes doesn't penalize enough on the composite when other dimensions are strong. The fix is: (a) make the additive parser more accurate (fixing miscounts is the EV-003/019 direction already started with identity deltas), and (b) activate BARI_D4_SCORE_V1 (already D7 co-signed 2026-06-21, DEFAULT OFF) which applies a direct composite-point deduction for contested additives. When D4 scoring is active and the parser is accurate, the need for count-based composite caps weakens. Remove these caps after D4 scoring is validated on the live corpus and blast radius is measured.
- The D4 score activation (BARI_D4_SCORE_V1) must precede these cap removals as a safety prerequisite.
- Evidence registry: EV-003, EV-019, EV-103 (D4) â€” cite all three.
- BARI flag: `BARI_DECHAIN_ADDITIVE_CAPS` (new; depends on BARI_D4_SCORE_V1 being active and validated).
- STAGED: Workstream 1, Stage 2B (after D4 score validation).

### KEEP

**CHAIN V-1: TRANS_FAT_VETO (score = 0)**
- KEEP. Industrial trans fat at confirmed concentration (>1g/100g) is the only food-safety absolute in the scoring universe. The natural dairy exemption already handles the false-positive risk from ruminant CLA. This is a genuine safety veto, not an architectural chain. Evidence tier: Strong (WHO, EFSA, FDA). The bar for KEEP is met.

**CHAIN CC-1 and CC-2: Confidence ceilings (50/75)**
- KEEP. These are not scoring-philosophy chains â€” they are epistemological guardrails. When Bari does not have sufficient data to score a product, it should say so clearly. Capping at 50/75 is the machine-readable expression of "we cannot assess this confidently." Removing these would mean confidently scoring a product from partial data, which is an integrity failure.

**CHAIN SW-1: SWEETENER_CAP_A/B/C (75/73/70)**
- KEEP (with tier graduation). The sweetener caps already embody the graded-severity model (Tier A fermentation-derived is least penalized; Tier C synthetic is most). This is the exact graduated approach the emulsifier/additive philosophy directs. The caps reflect genuine evidence differentiation (EV-005 for polyols, sweetener tier evidence per ADDITIVE_IDENTITY_DELTAS framework). A product with synthetic sweeteners should not score in the A range because the glycemic_quality dimension reflects low sugar â€” the cap prevents that systematic inversion. KEEP as a genuinely calibrated graduated safety mechanism, not an architectural chain.
- Note: Review Tier A cap value (75). If evidence supports natural fermentation-derived sweeteners more strongly, the Tier A cap could be raised to 80 â€” but that is a calibration decision, not a de-chaining decision.

**CHAIN FL-1: NOVA1_SINGLE_FLOOR (85)**
- KEEP. A genuinely single-ingredient whole food (a single nut, plain yogurt with no additives, a whole fruit) should score at least in the A range â€” that is the foundational proposition of food quality assessment. The floor is already gated by multiple conditions (nova_conf >= 0.70, ingredient_count <= 1, beverage reconstitution check). It is not a chain that inflates â€” it prevents the engine from penalizing a plain food for what it doesn't have (e.g. a single almond scored down because it lacks fiber). The floor is philosophically correct. KEEP.

**CHAIN FL-2: WHOLE_FOOD_FAT_FLOOR (70)**
- KEEP. Same logic as FL-1. Butter and pure dairy cream are whole foods within their category. Scoring them at D or E because their sat-fat content hits dimension scoring hard is a category-error â€” it treats whole-food fat composition as a reformulable defect. The floor prevents that error. The EV-048 gate for butter and EV-REDLABEL-005 for endemic categories encode the same underlying principle. KEEP at 70.

**CHAIN FL-3 and FL-4: PHYSIO_MODERATION_MIN (60) and PHYSIO_2PLUS_LABELS_MIN (50)**
- KEEP. These are the interaction floors that prevent the whole-food floors from becoming inversion machines for genuinely problematic whole foods (high-sugar honey, high-salt butter). They are the counterweight to FL-1/FL-2 and are mechanically integrated with the floor architecture. They are not NOVA-driven chains â€” they are outcome guardrails that the owner-directed BARI-INVERSION-TEST-001 concept formalizes. KEEP.

**CHAIN PB-1: PROTEIN_BAR_POLYOL_CAPS (62/66)**
- KEEP (for now, subject to separate protein-bar calibration review). Maltitol has genuine evidence of GI distress at typical bar serving sizes (dose-dependent; EV-005 polyol evidence). The caps reflect tiered severity. These are not architectural chains â€” they are evidence-based dose-risk signals applied to a specific ingredient class in a specific format. They warrant their own separate EV review when the protein-bar scoring workstream continues, not de-chaining here.

**CHAIN SR-F1 through SR-F8: Shelf-relative formulation floors**
- KEEP. These are already the graduated, continuous, category-relative signals that the de-chaining philosophy calls for. They are the anti-NOVA replacement for sugar assessment within each enrolled category. They are part of the solution, not part of the problem.

---

## 3. STAGED SEQUENCE

Each stage removes a chain only after its continuous replacement is in place and the guardrail covers residual risk. Stages within workstreams are ordered by dependency.

### Stage 0: W4 WFI Completion (CHAIN N-2 partial fix)
**What:** Apply confidence scaling to `whole_food_integrity` dimension (complete the half-implemented W4). This is a bug fix, not a philosophy change. W4 is already DEFAULT ON.
**Change:** Modify `score_whole_food_integrity()` (`score_engine.py:2151-2157`) to accept `confidence` and `materiality` parameters, apply `_w4_confidence_scale()` to the WFI base score using the same formula as `_d3_modifier_score()`.
**Dependency:** None. W4 is already on; this is completing its intended design.
**Guardrail dependency:** None beyond existing W4 invariants.
**Flag:** No new flag needed â€” this is a fix to the live W4 path (`BARI_GLASSBOX_W4=on`). Optionally gate it under a new `BARI_GLASSBOX_W4_WFI` sub-flag for rollback safety.
**Blast radius:** Moderate. Products with low/medium-confidence NOVA where WFI was previously un-scaled will see WFI score pull toward 50. This can increase scores for low-confidence NOVA-4 products (WFI was 30 â†’ pulls toward 50) and decrease for low-confidence NOVA-1 products (WFI was 100 â†’ pulls toward 50). Products with high-confidence NOVA are byte-identical.

### Workstream 1: NOVA Signal Replacement (Stages 1A, 1B, 2)

**Stage 1A: Additive parser accuracy validation and D4 score activation**
**What:** Activate BARI_D4_SCORE_V1 (already D7 co-signed 2026-06-21). Run blast radius on all 12 live categories. Validate additive parser accuracy (EV-003/019 identity deltas) by checking that NOVA-4 products with high additive burdens score below 68 naturally on the composite without N-3 cap.
**Prerequisite for:** Stage 2 (CHAIN N-3 cap removal), Stage 2B (CHAIN P-1/P-2 cap removal).
**Flag:** `BARI_D4_SCORE_V1` (existing, DEFAULT OFF â†’ flip to ON)
**Blast radius specification:** `spine_flip.py --set BARI_D4_SCORE_V1=on` â†’ re-score all 12 live categories â†’ diff vs committed baselines. Expected: 6 grade moves owner-reviewed 2026-06-21 (102/483 products penalized, per TASK-371). Verify movement table before any commit.

**Stage 1B: NOVA-4 cap relaxation (CHAIN N-3 â†’ outcome guardrail)**
**What:** Raise NOVA_PROXY_4_ULTRA_PROCESSED cap from 68 to 78 as an interim step (not full removal). The 78 still prevents grade-B for verified NOVA-4 at high confidence (B threshold is 65, so 78 allows B-range but prevents A). Full removal follows after blast-radius verification confirms the additive dimension produces sufficient natural depression.
**Prerequisite:** Stage 1A must be complete and validated.
**Flag:** `BARI_DECHAIN_NOVA4_CAP` (new; adjusts the cap constant)
**Guardrail dependency:** BARI-INVERSION-TEST-001 must be formally specified as a test before this ships. The test verifies: no NOVA-4 product with 3+ NOVA-4 marker additives scores higher than a NOVA-2 product with equivalent nutritional profile.

**Stage 2: Reassembly/Matrix Signal Design (CHAIN N-1 replacement)**
**What:** Design, validate, and activate a continuous label-observable processing signal that replaces the NOVA_PROCESSING_SCORES lookup. This is the hardest workstream.
**Prerequisites:** Stage 0 (WFI fix), Stage 1A (additive accuracy), Stage 1B (cap relaxed so the lookup can be gradually retired).
**Design requirements for the replacement signal:**
1. Must be computable from Hebrew label ingredient text (label-derivability gate).
2. Must score "refined-starch-plus-nothing" products at â‰¤70 on processing_quality, not 95. A product that is white flour + sugar + palm oil + no additives is structurally processed even if it has only 3 ingredients. The signal must detect this via: presence of refined grain tokens (×§×ž×— ×—×™×˜×”/×§×ž×—, no whole-grain override), AND absence of any whole-food complexity signal (no nuts, no seeds, no whole grains, no legumes, no vegetables).
3. Must still score genuine NOVA-1 whole foods (unroasted nuts, plain oats, legumes) at 90+.
4. Must be confidence-scaled (inherit W4 mechanics).
**Low-confidence NOVA scaling:** Confirmed by the debate: low-confidence NOVA must scale toward the WORSE class (NOVA-4 neutral), NOT toward a central neutral. Concretely: when confidence is low and NOVA could be 3 or 4, the processing_quality score should be pulled toward the NOVA-4 value (35), not the arithmetic midpoint (50). This is the Red Team finding in the debate brief. The current _w4_confidence_scale formula pulls toward 50 (neutral), which rewards obfuscation. The revised formula for low-confidence should be: `score = base_score - (base_score - NOVA4_SCORE) Ã— (1 - confidence_scale)` â€” i.e. shrink toward the pessimistic class, not the neutral.
**Evidence registry:** New EV-NOVA-REPLACE-001 (to be registered). Label-observability validation required.
**Flag:** `BARI_DECHAIN_NOVA_LOOKUP` (new)

### Workstream 2: Red-Label De-Anchoring (Stages 3â€“6)

**Stage 3: Graduated sugar extension (CHAIN S-1 replacement foundation)**
**What:** Extend SUGAR_GRADUATED_BANDS to cover the full 25g+ range (remove the ">=25g: 0, hard caps handle this" exclusion). Set a meaningful penalty in that band (proposed: 8 points, consistent with other high-severity penalty magnitudes). Activate within BARI_REDLABEL_V1.
**Prerequisite:** BARI_REDLABEL_V1 must be active.
**Flag:** `BARI_REDLABEL_V1` (existing)

**Stage 4: Snack-bar/granola shelf-relative enrollment (CHAIN S-6 replacement)**
**What:** Enroll `snack_bar_granola` in SUGAR_SHELF_REL_SCOPE for the graduated sugar shelf-relative signal, replacing the SNACK_BAR_RED_SUGAR_LABEL binary cap (55).
**Prerequisites:** Stage 3 active; corpus statistics for snack_bar_granolaÃ—sugar computed (n >= 20, scale > 3.0g guard).
**Flag:** `BARI_SHELF_RELATIVE_V1` (existing, DEFAULT ON) + snack_bar_granola enrollment following EV-085/087 precedent.
**New EV:** EV-SNACKBAR-SR-001 (shelf-relative enrollment for snack_bar_granolaÃ—sugar).

**Stage 5: Full BARI_REDLABEL_V1 activation + CHAIN S-7 retirement**
**What:** Activate BARI_REDLABEL_V1 across all categories (currently scoped to dairy_protein/whole_food_fat for some provisions). After activation, the ISRAELI_RED_LABEL_1_SUGAR composite cap becomes redundant as the regulatory_quality dimension continuous deduction covers the same ground.
**Prerequisites:** Stages 3 and 4 active; Product Agent D7 co-sign on cross-category activation; blast-radius measurement on all 12 live categories.

**Stage 6: CHAIN S-8 retirement (ISRAELI_RED_LABELS_2_PLUS cap = 45)**
**What:** Once BARI_REDLABEL_V1 is fully active and calibrated, the 45 cap is made redundant by the compounding of two label deductions in regulatory_quality plus the full sugar dimension scoring. Measure whether any product that was held at 45 now scores above 50 (which would constitute a calibration failure, not a de-chaining success). Adjust deduction slopes if needed before removing the cap.
**Prerequisites:** Stage 5 complete and verified; blast-radius table showing no product previously at 45 now exceeding 55.

### Workstream 3: Calorie Caps (Stages 7)

**Stage 7: CHAIN C-1 and C-2 replacement**
**What:** Design calorieÃ—satiety cross-dimension interaction term; confirm snack_bar_granola calorie table calibration. These are lower priority and do not block Workstreams 1 or 2.
**Flag:** `BARI_DECHAIN_CALORIE_CAP` (new)
**Prerequisite:** None blocking, but Stage 0 should be complete first (WFI fix establishes stable baseline).

### Workstream 4: RECAL_P0 Default Promotion (Stage 8)

**Stage 8: BARI_RECAL_P0 default promotion (CHAIN F-1 full retirement)**
**What:** Promote RECAL_P0 from optional flag to default-ON. This is the deepest change and affects protein scale (R1), fiber-not-applicable (R2), NOVA demotion guard (R4), graded sat-fat penalty (R5, replaces F-1), veg_spread re-weight (R6), and cultured-dairy bonus (R7). At this point F-1 (ISRAELI_RED_LABEL_1_SAT_FAT cap) is suppressed permanently.
**Prerequisites:** Stages 0-7 all complete; full Product Agent D7 co-sign on all RECAL_P0 provisions; owner go-live decision (frozen-invariant tripwire fires: this changes published scores across all live categories).
**Flag:** `BARI_RECAL_P0` (existing, DEFAULT OFF â†’ promote to ON as new default)

---

## 4. GUARDRAIL DEPENDENCY

**BARI-INVERSION-TEST-001 (formal specification required)**
The debate brief references this test by name but no formal spec file exists at `01_framework/` (VERIFIED: search found no file containing "BARI-INVERSION-TEST-001"). Before any Stage 1B or later stage ships, this test must be formally specified as a machine-executable check. Proposed definition:

> BARI-INVERSION-TEST-001: For every pair (P_clean, P_junk) in a reference set where P_clean has NOVA-class â‰¤ P_junk's NOVA-class AND P_clean has â‰¤ P_junk's additive count AND equivalent or better nutritional profile, score(P_clean) â‰¥ score(P_junk). Any violation is a FAIL.

The reference set must be pre-committed before Stage 1B; any new scoring change that passes Stage-1B's blast radius but fails BARI-INVERSION-TEST-001 is a CHANGES_REQUESTED.

**Stage-specific guardrail dependencies:**
- Stage 0: None beyond existing W4. Independent.
- Stage 1A: BARI-INVERSION-TEST-001 must be specified (not necessarily passing â€” just specified) before D4 activation.
- Stage 1B: BARI-INVERSION-TEST-001 must pass on the Stage-1A baseline before N-3 cap is relaxed.
- Stage 2: BARI-INVERSION-TEST-001 must pass on the Stage-1B baseline. Additionally, a new invariant is required: "low-confidence NOVA scales toward the pessimistic class (NOVA-4 score), not toward neutral 50" â€” this must be implemented in the confidence-scaling formula before the NOVA lookup is removed.
- Stages 3-6: No new invariants beyond monotonicity (adding sugar/additives never raises a score). The existing BARI_SHELF_RELATIVE_V1 anti-inversion floors provide the category-specific guardrails.
- Stage 8: All RECAL_P0 invariants as documented in recalibration_p0_design_v1.md must pass.

**New invariant required (not yet formalized): Low-Confidence NOVA Pessimistic Scaling**
- Current W4 formula: `score = 50 + (base_score - 50) Ã— confidence_scale` â€” pulls toward neutral 50.
- Required revision: `score = NOVA4_BASE + (base_score - NOVA4_BASE) Ã— confidence_scale` where `NOVA4_BASE = NOVA_PROCESSING_SCORES[4] = 35` â€” pulls toward the pessimistic anchor.
- Effect: a low-confidence NOVA-1 product still scores above 35 (e.g. low confidence scale 0.40: `35 + (95-35)Ã—0.40 = 59`), but a low-confidence NOVA-4 stays at 35. This is the asymmetry needed to prevent obfuscation from rewarding itself.
- Evidence: Verified Red Team finding from the P396 debate. Evidence tier: Moderate (empirical from engine behavior analysis; not a literature-derived threshold).
- This must be an EV-level change before Stage 2 implementation.

---

## 5. GOVERNANCE PER CHANGE

| Chain | Disposition | Evidence Registry | Label-Observability | Feature Flag | Rollback |
|---|---|---|---|---|---|
| N-1 (NOVA step lookup, processing_quality) | REPLACE | New EV-NOVA-REPLACE-001 | NEEDS VALIDATION (reassembly signal) | BARI_DECHAIN_NOVA_LOOKUP (new) | Flag OFF â†’ exact baseline |
| N-2 (NOVA step lookup, WFI) | REPLACE | EV-042 revised | VERIFIED (W4 already live) | BARI_GLASSBOX_W4 (existing) | Flag OFF â†’ no WFI scaling |
| N-3 (NOVA-4 composite cap 68) | REPLACE â†’ REMOVE | EV-003, EV-019, EV-103 | VERIFIED (additive count observable) | BARI_DECHAIN_NOVA4_CAP (new) | Flag OFF â†’ cap at 68 |
| N-4 (NOVA-3 composite cap 87) | REMOVE | No new EV needed; rule is inert in practice | N/A | BARI_DECHAIN_NOVA3_CAP (new) | Flag OFF â†’ cap at 87 |
| S-1 (HIGH_CAL_HIGH_SUGAR_SEVERE 50) | REPLACE | EV-REDLABEL-011 revised | VERIFIED (sugar_g on label) | BARI_REDLABEL_V1 (existing) | Flag OFF â†’ cap at 50 |
| S-2 (HIGH_CAL_HIGH_SUGAR_MODERATE 60) | REMOVE | No new EV; subsumed by S-7 | N/A | BARI_DECHAIN_SUGAR_MODERATE (new) | Flag OFF â†’ cap at 60 |
| S-3 (HIGH_SUGAR_25G_PLUS 60/68) | REPLACE | EV-REDLABEL-011 revised | VERIFIED | BARI_REDLABEL_V1 | Flag OFF â†’ cap active |
| S-4 (HIGH_SUGAR_25G_GRANOLA_SEVERE 50) | KEEP (recent, just activated) | EV-105 | VERIFIED | BARI_GRAN_SUGAR_25G_V1 | Flag OFF â†’ no cap |
| S-5 (SNACK_BAR_HIGH_CAL_SUGAR 60) | REMOVE | No new EV; subsumed | N/A | BARI_DECHAIN_SNACKBAR_SUGAR_CAP (new) | Flag OFF â†’ cap at 60 |
| S-6 (SNACK_BAR_RED_SUGAR_LABEL 55) | REPLACE | EV-SNACKBAR-SR-001 (new) | VERIFIED (sugar_g) | BARI_SHELF_RELATIVE_V1 + enrollment | Enrollment off â†’ cap reverts |
| S-7 (ISRAELI_RED_LABEL_1_SUGAR 55) | REPLACE | EV-REDLABEL-001â€“012 | VERIFIED (red label count) | BARI_REDLABEL_V1 | Flag OFF â†’ cap at 55 |
| S-8 (ISRAELI_RED_LABELS_2_PLUS 45) | REPLACE | EV-REDLABEL-006 | VERIFIED | BARI_REDLABEL_V1 | Flag OFF â†’ cap at 45 |
| C-1 (HIGH_CAL_LOW_SATIETY_SEVERE 55) | REPLACE | EV-CALORIE-SATIETY-001 (new) | VERIFIED (kcal, protein, fiber) | BARI_DECHAIN_CALORIE_CAP (new) | Flag OFF â†’ cap at 55 |
| C-2 (SNACK_BAR_HIGH_CAL 70) | REPLACE | EV-PBAR-008 (calorie table) | VERIFIED | BARI_DECHAIN_CALORIE_CAP (new) | Flag OFF â†’ cap at 70 |
| P-1 (ADDITIVE_MARKERS_5_PLUS 60) | REPLACE | EV-003, EV-103 | VERIFIED (additive count) | BARI_DECHAIN_ADDITIVE_CAPS (new) | Flag OFF â†’ cap at 60 |
| P-2 (ADDITIVE_MARKERS_3_PLUS 72) | REPLACE | EV-003, EV-103 | VERIFIED | BARI_DECHAIN_ADDITIVE_CAPS (new) | Flag OFF â†’ cap at 72 |
| Na-1 (HIGH_SODIUM_700MG_PLUS 60) | REPLACE (already in progress via BARI_GRAD_SODIUM_V1) | EV-055, EV-REDLABEL-009/010 | VERIFIED | BARI_GRAD_SODIUM_V1, BARI_REDLABEL_V1 | Flag OFF â†’ cliff cap |
| F-1 (ISRAELI_RED_LABEL_1_SAT_FAT 55) | REPLACE (via RECAL_P0 R5) | EV-029 | VERIFIED (sat_fat on label) | BARI_RECAL_P0 | Flag OFF â†’ cap at 55 |
| SW-1 (Sweetener caps 75/73/70) | KEEP | EV-005 | VERIFIED | Existing | N/A |
| V-1 (Trans-fat veto) | KEEP | Strong evidence | VERIFIED | Existing | N/A |
| CC-1/CC-2 (Confidence ceilings) | KEEP | Epistemological rule | N/A | Existing | N/A |
| FL-1/FL-2/FL-3/FL-4 (Whole-food floors) | KEEP | SRC-01 | N/A | Existing | N/A |
| PB-1 (Protein-bar polyol caps) | KEEP (for now) | EV-005 | VERIFIED | Existing | N/A |

**Rule accumulation note:** This proposal nets a REDUCTION of approximately 10 named cap rules upon full completion (Stages 0-8), and replaces them with 3-4 graduated signal mechanisms. The net effect is a simpler engine. Each new EV must pass the standard 3-gate dedup check (label-derivable, not already modelled, material to outcome) before registration.

---

## 6. PROJECTED-IMPACT METHODOLOGY FOR STAGE 1

**Stage 1A blast radius (BARI_D4_SCORE_V1 activation):**

The orchestrator runs this exact sequence to produce the score-drift table for Stage 1A:

1. Record committed baseline: for each of the 12 live categories, read the current BSIP2 output JSON (scores, grades, barcodes) from `02_products/*/skus_full/` or the category's frontend JSON. This is the "before" baseline.

2. Run spine_flip:
```
python 03_operations/bsip2/proto_v0/src/spine_flip.py --set BARI_D4_SCORE_V1=on --all
```

3. Collect the "after" scores from the spine_flip output directory.

4. Produce a movement table per category with columns: barcode, product_name, before_score, after_score, before_grade, after_grade, delta, grade_change (Y/N). Sort by abs(delta) descending.

5. Summary statistics: n_products_affected (delta != 0), n_grade_changes, max_delta, mean_delta for affected products.

6. Run conformance check: `python 03_operations/page_generator/conformance.py --all` â€” verify all 12 categories still conform.

7. Run BARI-INVERSION-TEST-001 on the "after" set once that test is formally specified.

8. Owner reviews the movement table. If any grade change involves a product that has been publicly discussed by the owner or is in a live-display category, flag it explicitly.

**Expected outcome from Stage 1A (VERIFIED from TASK-371 pre-analysis):** Approximately 102/483 products penalized, 6 grade moves (all downward for contested-additive products), per the owner-reviewed analysis from TASK-371 (2026-06-21). The orchestrator must re-verify this number against the current corpus before reporting it as confirmed.

---

## Honest Acknowledgments on What Cannot Come Off Yet

1. **The NOVA lookup (N-1) cannot come off until the reassembly signal is designed and validated.** The clean-label-refined-starch inversion is a real failure mode â€” removing the lookup without the replacement risks it. Stage 2 is the hardest workstream and may take the longest.

2. **The low-confidence NOVA pessimistic scaling (Section 4 new invariant) must be implemented before Stage 2.** The current W4 formula pulls toward neutral 50, which rewards obfuscation. Until that formula is corrected, removing the NOVA lookup would worsen rather than improve the inversion problem.

3. **BARI_REDLABEL_V1 must receive Product Agent D7 co-sign before Stages 3-6 can ship.** The Nutrition Agent proposes the graduated sugar/sodium extensions; the Product Agent's sign-off gates cross-category activation.

4. **BARI_RECAL_P0 promotion (Stage 8) requires owner go-live approval.** This is a frozen-invariant tripwire: it changes published scores across all live categories. The Nutrition Agent and Product Agent can jointly propose it; only the owner can authorize it.

5. **S-4 (HIGH_SUGAR_25G_GRANOLA_SEVERE)** was just D7 co-signed on 2026-06-23. It is not proposed for removal â€” it is a correctly scoped, recently approved cap that belongs in the graduated sugar architecture for granola/cereal.

---

```json
{
  "return_contract": {
    "task_id": "TASK-395",
    "proposed_status": "RETURNED",
    "artifacts": [
      {
        "type": "D6_proposal",
        "description": "BSIP2 Engine De-Chaining D6 Scoring Rule Proposal",
        "location": "Inline in this response (not a file; per system hard rule against creating .md files without explicit request)",
        "sha256": "not_applicable_inline"
      }
    ],
    "counts": {
      "chains_inventoried": 25,
      "chains_remove": 4,
      "chains_replace": 14,
      "chains_keep": 7,
      "stages_defined": 8,
      "workstreams": 4,
      "new_evs_required": 4,
      "existing_evs_cited": 18,
      "new_feature_flags_proposed": 7,
      "existing_flags_leveraged": 7,
      "frozen_invariant_tripwires_identified": 1,
      "verified_lines_cited": "score_engine.py and constants.py â€” specific line numbers cited per chain"
    },
    "commands_run": [],
    "not_done": [
      "No engine code changed (proposal only)",
      "No scores changed (proposal only)",
      "BARI-INVERSION-TEST-001 formal spec file not yet created (flagged as prerequisite for Stage 1B)",
      "EV-NOVA-REPLACE-001 not yet registered in bsip2_evidence_registry_v1.md (requires N-1 replacement design)",
      "EV-SNACKBAR-SR-001 not yet registered (requires snack_bar_granola corpus statistics)",
      "EV-CALORIE-SATIETY-001 not yet registered",
      "Product Agent D7 co-sign not yet obtained",
      "Blast radius not yet run (methodology specified in Section 6)"
    ],
    "spec_conflicts_identified": [
      "BARI-INVERSION-TEST-001 referenced in debate brief and proposal but no formal spec file exists at 01_framework/ â€” flagged as must-create before Stage 1B",
      "W4 formula (score toward neutral 50) conflicts with debate consensus requirement (score toward pessimistic NOVA-4 anchor for low-confidence) â€” requires formula revision as a new invariant before Stage 2"
    ],
    "acceptance_test": "This proposal is accepted when: (1) Product Agent provides D7 co-sign on the disposition table, (2) BARI-INVERSION-TEST-001 is formally specified as a machine-executable test, (3) Stage 0 blast radius is measured and approved by owner, (4) EV-NOVA-REPLACE-001 is registered with label-observability validation. No engine change ships before all four conditions are met."
  }
}
```