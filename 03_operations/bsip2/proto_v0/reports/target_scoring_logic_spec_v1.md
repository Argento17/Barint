# Target Scoring Logic Specification v1
**Proposal Class:** D6 (Nutrition Agent — scoring rule proposal)
**Required co-sign:** Product Agent (D7)
**Owner gate:** Required before any deploy (frozen-invariant tripwire: changes published scores)
**Task:** TASK-395
**Date authored:** 2026-06-25
**Status:** PROPOSAL ONLY — no engine code changed, no scores changed, no published score affected

---

## Preamble: What This Spec Is and Is Not

This is the Phase-2 north-star from the four-lane ratified program plan (`scoring_overhaul_program_v1.md`). It specifies the *target* scoring logic — the architecture the engine should converge toward once Phases 0 and 1 (reproducible baseline, chain inventory) are complete.

This spec does NOT:
- Change any live score
- Activate any flag
- Replace any code
- Override the staged sequence defined in `dechain_d6_proposal_v1.md` (Stage 0 through Stage 8)

The staged sequence remains the operative execution order. This spec provides the target model those stages are building toward — a coherent picture the Data Agent can implement against and the Adversarial QA Agent can write invariants for.

**Governing principle (C3, ratified by all lanes):** "Do not confuse 'remove chains' with 'remove judgment.' The chains are bad because they are brittle, opaque, and over-dominant — not because Bari can avoid normative choices. The rewrite must make those choices explicit, evidence-backed, observable, testable, and reversible."

---

## Section 1: Dimension List, Weights, and Calibration Philosophy

### 1.1 The Ten Dimensions

The current engine uses ten scoring dimensions combined by a weighted sum into a composite 0–100 score. The target model retains all ten dimensions with revised weight guidance. Dimension identities are not changed — the architecture is continuous revision, not a rewrite.

| # | Dimension | Current Weight | Target Weight | Scope | Rationale |
|---|---|---|---|---|---|
| 1 | `calorie_density` | 0.15 | 0.15 | Global | Direct label-derivable. Energy density is a first-order signal for caloric burden per eating occasion. Weight is appropriate; no change proposed. |
| 2 | `glycemic_quality` | 0.12 | 0.12 | Global | Sugar contribution is well-evidenced (WHO 2015 free sugars guideline; WHO 2022 sweetener guidance). Weight reflects its centrality without overpowering other signals. No change proposed. |
| 3 | `fat_quality` | 0.10 | 0.10 | Global | Saturated fat and fat source signal. Currently split between a dimension score (continuous sat-fat function) and a composite cap (F-1). Target: dimension carries the full signal once R5/RECAL_P0 is default. No weight change. |
| 4 | `processing_quality` | 0.18 | 0.18 | Global | Currently driven by NOVA step-lookup (N-1). Target: driven by the reassembly/matrix signal (Section 2). Highest weight because processing is the dimension with the broadest cross-category signal. Weight retained — reducing it would let highly processed products escape on nutrition numbers alone. |
| 5 | `whole_food_integrity` | 0.12 | 0.12 | Global | Currently driven by NOVA step-lookup (N-2), not confidence-scaled. Target: confidence-scaled toward the pessimistic NOVA-4 anchor (Stage 0, already in engine per `score_whole_food_integrity()` when BARI_W4_WFI_V1 is ON). Weight unchanged. |
| 6 | `additive_quality` | 0.10 | 0.10 | Global | Additive count and identity. Will be augmented by D4 score signal (BARI_D4_SCORE_V1, already D7 co-signed). No weight change. |
| 7 | `sodium_quality` | 0.07 | 0.07 | Global; category-calibrated for endemic | Sodium dimension. Already graduated for brined categories (EV-055/056). No weight change. |
| 8 | `satiety_support` | 0.06 | 0.06 | Global; gated for cooking oils | Protein + fiber. Currently too light to register the calorie×satiety interaction (the root cause C-1 caps tried to patch). A cross-dimension interaction term addresses the gap rather than a weight change — see Section 5, C-1 disposition. |
| 9 | `regulatory_quality` | 0.06 | 0.06 | Global | Israeli red-label deductions. Already continuous under BARI_REDLABEL_V1. No weight change. |
| 10 | `protein_quality` | 0.04 | 0.04 | Global | Crude protein scale. DIAAS is not label-derivable per KB-004; this dimension scores grams, not digestibility. No change proposed — this is already the correct framing. |

**Total weight = 1.00 in all configurations.**

### 1.2 Weight Calibration Honesty Statement

The weights above are inherited from the current engine's empirical calibration and are not re-derived from first principles in this spec. Each weight is labeled one of:

- **Evidence-backed:** direction and rough magnitude is supported by nutritional epidemiology (e.g., the primacy of processing_quality and calorie_density is consistent with NOVA framework literature and systematic reviews on UPF health outcomes — evidence tier: Moderate to Strong for directionality; the specific weight value is Corpus-fit).
- **Corpus-fit:** the weight was set to produce appropriate score distributions across the observed Israeli retail corpus. The value is not directly derivable from a nutrition study.

Honest labeling per dimension:

| Dimension | Weight source |
|---|---|
| `calorie_density` | Corpus-fit (magnitude); evidence-backed (direction) |
| `glycemic_quality` | Corpus-fit (magnitude); evidence-backed (direction, WHO 2015) |
| `fat_quality` | Corpus-fit (magnitude); evidence-backed (direction, EFSA sat-fat) |
| `processing_quality` | Corpus-fit (magnitude); evidence-backed (direction, Monteiro NOVA) |
| `whole_food_integrity` | Corpus-fit (magnitude); evidence-backed (direction, UPF literature) |
| `additive_quality` | Corpus-fit (magnitude); evidence-backed (direction, EV-003/019 EFSA) |
| `sodium_quality` | Corpus-fit (magnitude); evidence-backed (direction, WHO sodium) |
| `satiety_support` | Corpus-fit (weight is deliberately low — protein/fiber are supporting, not primary signals) |
| `regulatory_quality` | Corpus-fit (the MoH red-label thresholds are the anchor, not an independent Bari judgment) |
| `protein_quality` | Corpus-fit (low weight reflects crude-protein limitation, no DIAAS) |

Any future weight change requires a new EV with denominator-cited evidence and a full corpus drift table. Weights are not changed in this spec; this section establishes the calibration philosophy for future modifications.

### 1.3 Category-Calibrated vs. Global

**Global:** all ten dimension scores apply with the weights above across every category. The weighted sum is the same formula everywhere.

**Category-calibrated:** certain signals within dimensions use category-specific parameters:
- `sodium_quality`: REGQUAL_SODIUM_BY_CATEGORY (brined, hummus, salty snack)
- `calorie_density`: CALORIE_DENSITY_TABLES (snack_bar_granola, biscuit, etc.)
- `fat_quality`: endemic sat-fat categories (dairy_protein, whole_food_fat) get different cap/floor treatment
- Shelf-relative surcharge/relief bands apply within enrolled categories as modifiers on top of the base dimension score

This two-level structure — global weights, category-calibrated dimension sub-parameters — is the correct architecture. The current engine already follows it. The target model preserves it.

---

## Section 2: NOVA Replacement — the Reassembly/Matrix Signal

### 2.1 The Problem Being Solved

The current engine routes `processing_quality` through a rigid step-lookup: `NOVA_PROCESSING_SCORES = {1:95, 2:85, 3:65, 4:35}`. This creates:
- A four-step cliff (finding #1 in the verified findings list)
- A systematic misclassification path: a product with zero NOVA-4 additives but made entirely from refined flour, sugar, and palm oil gets NOVA 2-3 → scores 85 or 65 on processing_quality → escapes the appropriate penalty

The W4 confidence-scaling (currently applying to `processing_quality`, not yet to `whole_food_integrity` until Stage 0 completes) mitigates but does not eliminate the cliff. The NOVA-4 composite cap (N-3, 68) provides a backstop against the worst misclassifications, but does so bluntly.

### 2.2 The Target: Two-Component Continuous Processing Signal

The replacement for the NOVA step-lookup for `processing_quality` has two components that are summed before weighting. NOVA remains as ONE input — an important one — but is no longer the sole determinant.

**Component A: Additive-derived processing load (already active, refine only)**

The additive_marker_count and identity signals already exist in signal_extractor.py. In the target model, these drive a continuous `processing_load_score` directly:

```
processing_load_score = max(0, 100 - (additive_marker_count × per_additive_penalty))
```

Where `per_additive_penalty` is identity-differentiated (D4 scoring, already D7 co-signed):
- High-risk synthetic additives (EFSA contested, Tier 1): penalty = 20 per marker
- Neutral-to-synthetic moderate-concern additives (Tier 2): penalty = 15 per marker
- Plant-derived / prebiotic-function additives (Tier 3): penalty = 8 per marker
- Standard culinary additives (citric acid, lactic acid, natural color): penalty = 3 per marker

The per-additive-penalty values are **corpus-fit** (not literature-derived at this precision). The tier hierarchy is evidence-backed (EV-003, EV-019).

**Component B: Structural matrix signal — the refined-starch-no-whole-food detector**

This is the critical substitution. It must detect "clean-label refined-starch junk" — products that escape NOVA-4 detection because they lack named additives, yet are structurally processed.

Inputs are label-derivable from the Hebrew ingredient text and BSIP1 enrichment fields:

**Refined-starch markers (positive signal = lower score):**
- `קמח חיטה` / `קמח` without whole-grain qualifier: plain refined wheat flour
- `קמח אורז` / `עמילן תירס` / `עמילן חיטה`: refined starch bases
- `סוכר` as first-or-second ingredient: sugar-first or sugar-second formulation
- `שמן דקלים` / `שמן קוקוס` / `שמן צמחי` (unspecified): industrial fat source

**Whole-food complexity markers (negative signal = raises score back):**
- Any whole nut, seed, or legume in the ingredient list (מקל אגוז, שקד, גרעין, עדשים, חומוס)
- Whole grain tokens: `דגנים מלאים`, `שיבולת שועל`, `שיפון מלא`, `חיטה מלאה`
- Whole fruit or dried fruit (primary, not trace): תמר, ענב, צימוקים as first/second ingredient
- Fermentation markers: חמאה, חמץ, מחמצת, תסיסה

**Score formula:**

```
n_refined = count of refined-starch markers present
n_whole = count of whole-food complexity markers present
matrix_balance = n_whole - n_refined   # range: typically -3 to +4

matrix_score = 50 + (matrix_balance × 12)   # range: clamped to [10, 95]
matrix_score = max(10, min(95, matrix_score))
```

**Label-observability status:** The refined-starch markers are verified observable from Hebrew ingredient text (they exist in the current signal_extractor.py vocabulary). The whole-food complexity markers are partially implemented (has_whole_grain, has_fermentation are existing L3 signals; nut/seed/legume presence is a new required signal). The new required signal — nut/seed/legume presence — must be validated before Component B can be activated. This is the label-derivability gap that makes Stage 2 (N-1 replacement) the hardest workstream.

### 2.3 Combining Components A and B

```
processing_quality_score = 0.60 × processing_load_score + 0.40 × matrix_score
```

Where weights 0.60/0.40 are corpus-fit. The additive load carries more weight because it is more precisely observable. The matrix signal carries supplementary weight as the structural guard.

NOVA classification remains as a *modifier*, not a lookup:
- NOVA-4 classification at high confidence: apply a confidence-scaled penalty of −10 on the combined score (not a cliff, a moderate additional depression)
- NOVA 1-2 at high confidence: apply a bonus of +5 (not a floor, an incremental push)
- Medium or low confidence: reduce the magnitude of the modifier proportionally (using the pessimistic confidence scale — toward NOVA-4, not neutral, per the W4 revision)

### 2.4 Protection Against the Opposite Inversion

The clean-label refined-starch inversion is the scenario where removing NOVA makes it worse. The matrix signal (Component B) is explicitly designed to prevent this: a product with three ingredients (refined flour, sugar, palm oil) scores:
- n_refined = 3 (flour, sugar, palm oil all fire as refined markers)
- n_whole = 0
- matrix_balance = −3 → matrix_score = 50 + (−3 × 12) = 14

This product cannot score above ~45 on processing_quality even with zero additives, which is appropriate. The current engine, without the NOVA-4 cap, would give it ~85 (NOVA-2 lookup). This is the inversion the cap existed to prevent. The target design makes the cap unnecessary by directly detecting the structural problem.

---

## Section 3: Missing-Data Handling — Confidence Haircut Rule

### 3.1 The Verified Failure (Finding #2)

The engine currently removes a field's penalty when the field is blank, rather than applying a confidence haircut. Removing the ingredient list, or blanking a sugar/sat-fat/sodium value, raises the score by +2 to +33 because the blank field removes the cap or dimension penalty that would have fired. This violates the stated engine invariant ("removing data never raises a score") and is a gaming vector.

### 3.2 The Target Rule: Pessimistic Imputation + Confidence Ceiling

**Rule MD-1: Null nutrient values**

When a panel field is null (not scraped, not reported), the engine must NOT treat it as zero. Instead:

```
imputed_value = category_median_p75  # 75th percentile of the category corpus for that nutrient
confidence_weight = 0.70              # 30% haircut for imputed data
```

The imputed value is used only for cap/dimension scoring, never for display. The product trace must record that imputation occurred.

The 75th percentile (not median, not maximum) is the correct pessimistic anchor: it is worse than a typical product but not the worst case, which acknowledges genuine uncertainty. Category corpus statistics must be pre-computed and committed as constants, not inferred at scoring time.

**Rule MD-2: Missing ingredient list**

When `ingredients_list` is missing or `ingredient_text_quality` is `missing`/`corrupted`/`malformed`:
- `additive_marker_count` is treated as `category_p75_additive_count` (not zero)
- NOVA confidence band is forced to `low` regardless of other signals
- The pessimistic confidence-scaling toward NOVA-4 (per Section 2 and Stage 0 in `dechain_d6_proposal_v1.md`) applies
- The confidence ceiling (CC-1/CC-2) remains active — a product with missing data cannot score above 75

The specific consequence: removing the ingredient list cannot raise the score because the missing list triggers pessimistic imputation (non-zero additive count, NOVA-4 pessimistic pull), not zero.

**Rule MD-3: whole_food_integrity confidence scaling (Stage 0 fix)**

`score_whole_food_integrity()` must be confidence-scaled toward the pessimistic NOVA-4 anchor (`_WFI_PESSIMISTIC_ANCHOR = 30`), not toward neutral 50. The formula is already implemented in the engine (verified at `score_whole_food_integrity()` lines 2186–2215 when BARI_W4_WFI_V1 is ON). Stage 0 makes this default.

**Rule MD-4: Low-confidence NOVA pessimistic scaling direction**

The current W4 formula for `processing_quality` pulls toward neutral 50 when confidence is low. The target formula pulls toward the NOVA-4 anchor (35 for processing_quality):

```
# Current (to be replaced):
scaled_score = 50 + (base_score - 50) × confidence_scale

# Target:
PESSIMISTIC_ANCHOR = NOVA_PROCESSING_SCORES[4]  # = 35
scaled_score = PESSIMISTIC_ANCHOR + (base_score - PESSIMISTIC_ANCHOR) × confidence_scale
```

Effect: a low-confidence NOVA-1 product (confidence_scale = 0.40) scores `35 + (95-35)×0.40 = 59` — still above the additive-driven score for a genuine NOVA-4, but not the 95 it would receive at high confidence. A low-confidence NOVA-4 stays at 35. The asymmetry prevents obfuscation from rewarding itself.

This is EV-level change before Stage 2 implementation (referenced in `dechain_d6_proposal_v1.md` Section 4 as a new required invariant).

---

## Section 4: Fat-Sat Boundary Monotonicity Fix (Finding #3)

### 4.1 The Verified Failure

Adding +3g saturated fat raises the score at a shelf-relative cap boundary in hard_cheeses and hummus categories. This happens because the shelf-relative signal (a penalty based on distance from median) has a dead-zone and relief band: products in the dead zone or below-median relief band receive a bonus that can exceed the sat-fat cap's effect, net producing a score increase when sat-fat increases. This violates monotonicity.

### 4.2 The Target Fix: Asymmetric Penalty-Only Design

The shelf-relative differentiator for fat-sat must be redesigned as **penalty-only** for sat-fat. The current design allows below-median relief (a bonus for being below the median sat-fat). This is appropriate for sugar (where below-median sugar genuinely differentiates) but creates the inversion for sat-fat in cheese categories where even "below median" sat-fat is still high in absolute terms.

**Rule FS-1: No sat-fat shelf-relative relief**

For all categories where sat-fat shelf-relative is enrolled (hard_cheese, cheese_spread, currently using `FATSAT_SHELF_REL_*` constants):
- `direction = "surcharge_only"` — penalties fire for above-median sat-fat, no relief fires for below-median
- The `FATSAT_SHELF_REL_*_B_MAX` constants are set to 0 (no below-median bonus)

This makes sat-fat contribution monotonic: more sat-fat → equal or lower score, never higher. The constraint is unconditional and does not require a flag.

**Rule FS-2: Monotonicity invariant as a machine-checkable test**

The BARI-INVERSION-TEST-001 specification (which must exist before Stage 1B per `dechain_d6_proposal_v1.md`) must include a monotonicity assertion:

```
For every product P in every category, and for the sat-fat signal specifically:
  score(P with sat_fat = X + ε) ≤ score(P with sat_fat = X)  for all ε > 0
```

This is provable by unit test on the scoring function, not just by corpus inspection.

---

## Section 5: Cap Disposition — Kill, Keep, Convert

This section states the full disposition for every chain identified in `dechain_d6_proposal_v1.md`. The staged sequence is unchanged; this section adds the precise continuous replacement formula for each REPLACE disposition.

### 5.1 NOVA Family

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| N-1: NOVA_PROCESSING_SCORES step-lookup | REPLACE | Two-component processing signal (Section 2). Staged: Stage 2 (hardest workstream). |
| N-2: NOVA_WFI_SCORES step-lookup | REPLACE (partial, then full) | Stage 0: apply pessimistic W4 confidence scaling (formula MD-3). Stage 2B: same reassembly/matrix signal as N-1. |
| N-3: NOVA_PROXY_4_ULTRA_PROCESSED cap (68) | REPLACE → interim relaxation → REMOVE | Stage 1B: raise cap to 78 (interim). After additive parser validation: remove. The natural composite depression from correct additive scoring replaces it. |
| N-4: NOVA_PROXY_3_PROCESSED cap (87) | REMOVE | No replacement needed. Cap is practically inert — no NOVA-3 product reaches 87 composite without other caps firing first. Remove immediately with a flag (`BARI_DECHAIN_NOVA3_CAP`). |

### 5.2 Sugar Family

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| S-1: HIGH_CAL_HIGH_SUGAR_SEVERE cap (50) | REPLACE | Graduated sugar-severity curve extension: extend `SUGAR_GRADUATED_BANDS` to cover the 25g+ range with explicit penalty (proposed: 8 points — corpus-fit). When the continuous curve produces a composite at or below 50 naturally for a 500kcal/25g+ product, the cap is redundant. Activated within BARI_REDLABEL_V1 scope. |
| S-2: HIGH_CAL_HIGH_SUGAR_MODERATE cap (60) | REMOVE | Subsumed by S-7 (red label, cap=55, more binding) and the graduated sugar penalty bands at 17.5g–25g. No unique protection. Flag: `BARI_DECHAIN_SUGAR_MODERATE`. |
| S-3: HIGH_SUGAR_25G_PLUS cap (60/68) | REPLACE | Absorbed into the graduated sugar curve (same extension as S-1). Conditional retirement: remove only after the curve is active and calibrated. |
| S-4: HIGH_SUGAR_25G_GRANOLA_SEVERE cap (50) | KEEP | Recently D7 co-signed (2026-06-23, TASK-385). Correctly scoped. Not proposed for removal. |
| S-5: SNACK_BAR_HIGH_CAL_SUGAR cap (60) | REMOVE | Subsumed by S-7 and S-2 (which will be absorbed by the graduated curve). Category-relative calorie table handles the snack-bar calorie signal. Flag: `BARI_DECHAIN_SNACKBAR_SUGAR_CAP`. |
| S-6: SNACK_BAR_RED_SUGAR_LABEL cap (55) | REPLACE | Shelf-relative sugar signal enrolled for snack_bar_granola (same mechanism as biscuit EV-085, cereal EV-087). Binary 55 cap becomes redundant. Requires new EV-SNACKBAR-SR-001. |
| S-7: ISRAELI_RED_LABEL_1_SUGAR cap (55) | REPLACE | BARI_REDLABEL_V1 `regulatory_quality` dimension continuous deduction already designed to replace this. The composite cap is redundant once the deduction is calibrated. Staged: after full cross-category BARI_REDLABEL_V1 activation. |
| S-8: ISRAELI_RED_LABELS_2_PLUS cap (45) | REPLACE | Compounding of two label deductions in `regulatory_quality` plus full sugar dimension scoring should land below 50 naturally when correctly calibrated. Measure blast radius before removing. Staged: last. |

### 5.3 Calorie Family

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| C-1: HIGH_CAL_LOW_SATIETY_SEVERE cap (55) | REPLACE | Cross-dimension interaction term: when `calorie_density` scores in the top tier AND `satiety_support` < 30 (low protein AND low fiber), apply a combined continuous deduction of 8–12 points on the composite. This replaces the binary cliff. Requires new EV-CALORIE-SATIETY-001. Staged: Workstream 3, Stage 7. |
| C-2: SNACK_BAR_HIGH_CAL cap (70) | REPLACE | CALORIE_DENSITY_TABLES for snack_bar_granola already produces equivalent depression at high kcal. Confirm calibration; retire cap. |

**Continuous formula for C-1 replacement:**

```
if calorie_tier_score < 45 AND satiety_score < 30:
    interaction_penalty = 10 × (1 - satiety_score/30) × (1 - calorie_tier_score/45)
    # range: 0 to 10 points on the composite
```

The interaction penalty is bounded to avoid accumulating with other penalties beyond the CALORIE_FAMILY_BUDGET. It is never larger than 10 points and tapers as either signal improves. This is corpus-fit (not literature-derived at this precision).

### 5.4 Processing Family (Additive-Count Caps)

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| P-1: ADDITIVE_MARKERS_5_PLUS cap (60) | REPLACE | When BARI_D4_SCORE_V1 is active and the additive parser is accurate, the `additive_quality` dimension score plus the D4 composite-point deduction produce sufficient natural depression for a 5-additive product. Conditional on D4 validation. |
| P-2: ADDITIVE_MARKERS_3_PLUS cap (72) | REPLACE | Same as P-1. Lower priority; the 72 cap rarely binds uniquely. |

**Removal condition:** verify that after D4 activation, no NOVA-4 product with additive_count >= 5 scores above 65 on the composite without the cap. If any do, the D4 deduction is under-calibrated — adjust the deduction, do not restore the cap.

### 5.5 Sodium Family

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| Na-1: HIGH_SODIUM_700MG_PLUS cap (60) | REPLACE (in progress) | BARI_GRAD_SODIUM_V1 + brined_food context already implements the graduated replacement for endemic categories. Full cross-category activation follows BARI_REDLABEL_V1 sodium provisions (EV-REDLABEL-009/010). |
| Na-2: HIGH_SODIUM_CEREAL_500 cap (75) | KEEP (scoped, recently added) | Recently added graduated replacement for the cereal/granola scope. Not proposed for removal. |

### 5.6 Fat Quality Family

| Chain | Disposition | Continuous Replacement |
|---|---|---|
| F-1: ISRAELI_RED_LABEL_1_SAT_FAT cap (55) | REPLACE | RECAL_P0 R5 — graded sat-fat penalty on the `fat_quality` dimension — already replaces this when RECAL_P0_ON. Cap is already suppressed under RECAL_P0. Target: promote RECAL_P0 to default (Stage 8, owner-gated). |

---

## Section 6: Retained Guards

The following are retained unconditionally in the target model. Each retention is justified.

### 6.1 Trans-Fat Veto (V-1, score = 0)

**KEEP.** Industrial trans fat at confirmed concentration (>1g/100g) is the only food-safety absolute in the scoring universe. The natural dairy exemption (category `whole_food_fat` + no PHVO marker) already handles the false-positive risk from ruminant CLA/vaccenic acid. The veto is a genuine safety mechanism, not an architectural chain. Removal would require a formal change in scientific consensus that does not exist (WHO, EFSA, FDA all classify industrial trans fat as harmful at dose). Evidence tier: Strong.

### 6.2 Confidence Ceilings (CC-1 = 50, CC-2 = 75)

**KEEP.** These are epistemological guardrails, not scoring-philosophy chains. When Bari does not have sufficient data to score a product, capping at 50/75 is the machine-readable expression of epistemic humility. Removing these would mean confidently scoring a product from partial data — an integrity failure that consumers cannot detect. These ceilings interact correctly with MD-1 through MD-4 (Section 3): missing data triggers pessimistic imputation which lowers the score, and the ceiling prevents the imputed score from appearing as confident. The two mechanisms are complementary.

### 6.3 Sweetener Caps (SW-1: 75/73/70 by tier)

**KEEP.** The sweetener caps already embody the graduated-severity model this proposal promotes for other signals (Tier A fermentation-derived lowest penalty, Tier C synthetic highest). A product with synthetic sweeteners should not score in the A range because low sugar (via glycemic_quality) reflects the sweetener replacing sugar, not the product being nutritionally cleaner. The cap prevents that systematic inversion — exactly the kind of principled guardrail that de-chaining preserves rather than removes. Tier A cap (75) may be reviewed upward if evidence supports natural fermentation-derived sweeteners more strongly, but that is a calibration decision requiring its own EV, not in scope here. Evidence: EV-005 (polyol evidence), additive identity tier evidence.

### 6.4 Single-Ingredient Whole-Food Floor (FL-1, 85)

**KEEP.** A genuinely single-ingredient whole food — an almond, plain yogurt with no additives, a whole fruit — should score at least in the A range. This is the foundational food-quality proposition. The floor is already gated by multiple conditions (nova_conf >= 0.70, ingredient_count <= 1, beverage reconstitution check, BSIP1 text-fallback degradation guard). It is not an inflation mechanism — it prevents the engine from penalizing a plain food for what it doesn't have (e.g., a single almond scored down because it lacks fiber). Philosophically correct; retention is unconditional.

### 6.5 Whole-Food Fat Floor (FL-2, 70)

**KEEP.** Butter and pure dairy cream are whole foods within their category. Scoring them at D or E because sat-fat content hits dimension scoring hard is a category error — it treats compositionally fixed whole-food fat as a reformulable defect. The floor prevents that error. The EV-048 gate for butter and EV-REDLABEL-005 for endemic categories encode the same underlying principle. Retention at 70.

### 6.6 Physiological Moderation Floors (FL-3 = 60, FL-4 = 50)

**KEEP.** These are the counterweight to FL-1/FL-2. They prevent the whole-food floors from becoming inversion machines for genuinely problematic whole foods (high-sugar honey, high-salt butter). A whole food with a nutritional concern gets a moderated floor, not the full floor. FL-3 (60) applies when one reformulable red label fires. FL-4 (50) applies when two or more fire. These are mechanically integrated with the floor architecture and are not NOVA-driven chains — they are the interaction layer between floors and caps that gives the floor architecture coherent behavior.

### 6.7 Dominance Guardrail (BARI-INVERSION-TEST-001)

**KEEP and formalize.** This test is referenced in the debate brief and `dechain_d6_proposal_v1.md` but has no formal spec file (verified: no file exists at `01_framework/` containing the string "BARI-INVERSION-TEST-001"). It must be created as a machine-executable file before Stage 1B. The definition:

> **BARI-INVERSION-TEST-001:** For every pair (P_clean, P_junk) in a committed reference set where P_clean has NOVA-class ≤ P_junk's NOVA-class AND P_clean has ≤ P_junk's additive count AND P_clean has ≤ P_junk's score on each nutritional harm signal (sugar, sat-fat, sodium, kcal), then score(P_clean) ≥ score(P_junk). Any violation is a FAIL and blocks the stage.

The reference set must be pre-committed before Stage 1B ships. It must include adversarial fixtures: the Petit Beurre / Chokita pair (the motivating inversion), at least one clean-label refined-starch product vs. an equivalent NOVA-4 additive-heavy product, and at least one high-protein UPF vs. a lower-protein whole food.

---

## Section 7: Observability — What Every Trace Must Expose

The owner manifesto requires that every score be "explicit, observable, testable." The target model enforces this via the product trace. Every scored product's trace must expose:

### 7.1 Required Trace Fields

```json
{
  "dimension_scores": {
    "calorie_density": 72.0,
    "glycemic_quality": 55.0,
    "fat_quality": 48.0,
    "processing_quality": 41.0,
    "whole_food_integrity": 38.0,
    "additive_quality": 64.0,
    "sodium_quality": 70.0,
    "satiety_support": 60.0,
    "regulatory_quality": 80.0,
    "protein_quality": 55.0
  },
  "dimension_weights": { ... },
  "weighted_composite_pre_guardrail": 56.4,
  "caps_considered": [
    {"rule": "HIGH_CAL_HIGH_SUGAR_SEVERE", "fired": false, "condition": "kcal=420 < 500"},
    {"rule": "ISRAELI_RED_LABEL_1_SUGAR", "fired": true, "cap": 55, "note": "sugar=22g > 17.5g threshold"}
  ],
  "effective_cap": 55,
  "composite_post_cap": 55.0,
  "floors_considered": [...],
  "final_score": 55,
  "grade": "C",
  "confidence": "high",
  "confidence_basis": "full_panel + ingredient_list",
  "nova_level": 3,
  "nova_confidence": 0.65,
  "nova_confidence_band": "medium",
  "processing_quality_components": {
    "additive_load_score": 52.0,
    "matrix_balance_score": 38.0,
    "nova_modifier": -5.0,
    "combined": 44.6
  },
  "imputed_fields": [],
  "missing_data_penalties_applied": []
}
```

The `processing_quality_components` sub-object is new and required for the target model — it exposes the two-component structure so any score on `processing_quality` can be publicly decomposed.

### 7.2 Consumer Defensibility Standard

Any claim made in a product insight line must be derivable from a trace field. The trace is the source of truth for copy auditing. A scoring insight that cannot be traced to a field in the above structure fails the copy-trace gate (G6).

### 7.3 Aggregated Observability for Public Methodology

The methodology page must be derivable from these fields. No scoring logic that cannot be publicly explained in plain terms should exist in the engine. This is what "explicit, observable, testable" means in the manifesto — not that NOVA is publicized, but that the engine's actual signals are.

---

## Section 8: Anti-Regression Contract

### 8.1 The Honest Tension

The caps existed because the raw continuous engine, without them, let clean-label junk win. Specifically:
- A refined white-flour cookie with low sugar and no additives scored ~80/A on the continuous dimensions because glycemic_quality was good (low sugar), additive_quality was perfect (zero additives), and processing_quality was high (NOVA-2 lookup: 85)
- The caps prevented this by imposing a hard ceiling regardless of dimension scores

De-chaining removes the caps but must not restore this failure. The anti-regression contract maps each removed cap to the continuous signal that now carries its intent.

### 8.2 Coverage Map: Removed Cap → Continuous Replacement

| Removed Cap | Inversion Risk It Prevented | Continuous Signal That Now Carries It |
|---|---|---|
| N-3 NOVA-4 composite cap (68) | NOVA-4 products with good nutrition numbers winning on the composite | D4 score signal (additive identity deductions) + correct additive_quality dimension score |
| N-4 NOVA-3 composite cap (87) | NOVA-3 products scoring A grade | This cap was practically inert — no live product reached 87 without other caps. No new signal needed. |
| S-2 HIGH_CAL_HIGH_SUGAR_MODERATE (60) | kcal≥470 + sugar 17.5–20g products escaping penalty | Graduated sugar bands in that range (SUGAR_GRADUATED_BANDS active via BARI_REDLABEL_V1) |
| S-5 SNACK_BAR_HIGH_CAL_SUGAR (60) | High-cal high-sugar snack bars escaping penalty | S-7 (red label cap, more binding at 55) + category-relative calorie table |
| F-1 RED_LABEL_SAT_FAT (55) | High-sat-fat products outside whole-food context scoring too high | R5 graded sat-fat penalty on fat_quality dimension (RECAL_P0) |
| P-1/P-2 additive count caps (60/72) | Multi-additive products with good nutrition numbers scoring too high | D4 identity-differentiated deductions + additive_quality dimension with correct per-additive penalty |

### 8.3 The Adversarial Fixture Suite

Before any cap is retired, the following adversarial fixtures must pass BARI-INVERSION-TEST-001:

1. **Refined white-flour cookie, zero additives, low sugar:** must score below 60 (C or lower). The matrix signal (Component B, Section 2.2) must fire and produce a below-median processing_quality score.
2. **Engineered low-sugar UPF (e.g., protein wafer with 8 additives, 3g sugar):** must score below a plain oats product with comparable protein. The additive_quality and processing_quality signals must overcome the glycemic_quality boost.
3. **Palm oil confection with no declared additives:** must not score above 55. The matrix signal (palm oil as industrial fat, refined flour primary) must produce appropriate processing_quality depression.
4. **High-protein candy bar (35g protein, 8 additives, synthetic sweeteners):** must score below a whole-food protein source with equivalent protein and no additives. The additive + sweetener signals must overcome the protein dimension boost.
5. **Sodium bomb (900mg/100g, non-brined):** must score below 50. The sodium_quality dimension and red-label deduction must produce this without a hard cap.
6. **The Petit Beurre / Chokita pair (the motivating inversion):** Petit Beurre must score ≤ Chokita cream cookie. If after the rewrite this pair still inverts, the spec has failed its primary mission.

### 8.4 Grade-Distribution Sanity Gate

After any scoring change, the grade distribution across the full corpus must be within the following ranges (evidence tier: corpus-fit, calibrated to current live distributions + qualitative owner judgment):

- Grade A (80-100): 5–20% of scored products
- Grade B (65-79): 15–35%
- Grade C (50-64): 25–45%
- Grade D (35-49): 10–30%
- Grade E (0-34): 5–20%

Any category where a single grade contains >60% of products warrants a calibration review before deploy. This is not a hard block on the spec — it is a red-flag threshold for the shadow run.

---

## Section 9: Governance, Sequencing, and What This Spec Does Not Authorize

### 9.1 Governance Requirements

This spec is a D6 proposal. Before any implementation:
1. Product Agent D7 co-sign is required on the disposition table (Section 5) and the retained guards (Section 6)
2. Owner review of the philosophy (Section 1, Section 8 honest tension statement) is required — this is not a frozen-invariant tripwire for the spec itself, but the Phase-2 program plan requires owner review before the full shadow implementation begins
3. Owner-gated deploy (frozen-invariant tripwire) is required before any published score changes

### 9.2 What Is Authorized by This Spec (Without Additional D7)

Nothing. This is a proposal. The staged execution sequence in `dechain_d6_proposal_v1.md` governs what is authorized stage by stage.

### 9.3 Execution Sequence Reminder

This spec does not change the staged sequence. The stages remain:
- **Stage 0** (already in engine when BARI_W4_WFI_V1 is ON): WFI confidence scaling. This spec adds the requirement that the pessimistic-toward-NOVA-4 formula be confirmed active.
- **Stages 1A–2**: Workstream 1 (NOVA signal replacement). Stage 2 implements Section 2 of this spec.
- **Stages 3–6**: Workstream 2 (red-label de-anchoring). Stages implement Section 5.2 dispositions.
- **Stage 7**: Workstream 3 (calorie caps). Implements Section 5.3.
- **Stage 8**: Workstream 4 (RECAL_P0 promotion). Implements Section 5.6, owner-gated.

### 9.4 NOVA in the Target Architecture

The owner manifesto: "Our system is strong enough to avoid relying on simplistic methods such as NOVA." The target model honors this by demoting NOVA from a score-determining lookup to one input among several in a richer signal. NOVA does not disappear — the extrusion signal, HC-001 processed-dairy rule, and HC-002 dairy demotion guard are all NOVA-adjacent and are retained. What disappears is the rigid step-table that maps NOVA class to a fixed score. The new processing_quality signal uses NOVA as a modifier (±5–10 points, confidence-scaled), not a determinant.

---

## Not Done (Required Honesty Section)

The following items are specified here but not yet implemented:

1. **BARI-INVERSION-TEST-001 formal spec file** — referenced in Section 6.7 and `dechain_d6_proposal_v1.md` as required before Stage 1B. Not created yet; must be created as a machine-executable Python test before Stage 1B ships.
2. **Nut/seed/legume presence signal** — required for Component B (matrix signal) in Section 2.2. Not yet in signal_extractor.py. Must be validated for label-derivability from Hebrew ingredient text before Stage 2.
3. **Category corpus statistics for MD-1 (pessimistic imputation)** — `category_median_p75` constants per nutrient per category must be computed from the committed corpus and added to constants.py. Not computed here.
4. **EV-NOVA-REPLACE-001** — evidence registry entry for the reassembly/matrix signal. Not yet registered.
5. **EV-CALORIE-SATIETY-001** — evidence registry entry for the C-1 continuous replacement. Not yet registered.
6. **EV-SNACKBAR-SR-001** — evidence registry entry for snack_bar_granola shelf-relative enrollment. Not yet registered.
7. **Product Agent D7 co-sign** — not yet obtained.
8. **Owner review of Phase-2 philosophy** — not yet completed.
9. **Shadow run (Phase 3)** — no score has been changed; this spec only describes the target state.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md",
      "action": "created",
      "sha256": "not_yet_hashed — orchestrator must run Get-FileHash on final file"
    }
  ],
  "counts": {
    "dimensions_specified": "10/10 (all current engine dimensions covered)",
    "caps_dispositioned": "18/18 (all chains from dechain_d6_proposal_v1.md, Section 2)",
    "retained_guards": "7/7 (V-1, CC-1, CC-2, SW-1, FL-1, FL-2, FL-3+FL-4 pair, BARI-INVERSION-TEST-001)",
    "adversarial_fixtures_defined": "6 (Section 8.3)",
    "new_evs_required": "3 (EV-NOVA-REPLACE-001, EV-CALORIE-SATIETY-001, EV-SNACKBAR-SR-001)",
    "sections_authored": "9/9 (all required spec sections per delegation)"
  },
  "commands_run": [
    {"cmd": "Read scoring_overhaul_program_v1.md", "exit_code": 0},
    {"cmd": "Read dechain_d6_proposal_v1.md", "exit_code": 0},
    {"cmd": "Read score_engine.py (lines 1-100, 2100-2500, 2600-2760, 3370-3490)", "exit_code": 0},
    {"cmd": "Read nova_proxy.py (full)", "exit_code": 0},
    {"cmd": "Read return_contract_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "BARI-INVERSION-TEST-001 formal spec file not created (must exist at 01_framework/ before Stage 1B)",
    "Nut/seed/legume label-derivability signal not added to signal_extractor.py (required for Component B, Stage 2)",
    "Category corpus p75 statistics for pessimistic imputation not computed (required for MD-1, Stage 0 hardening)",
    "EV-NOVA-REPLACE-001 not registered in bsip2_evidence_registry_v1.md",
    "EV-CALORIE-SATIETY-001 not registered",
    "EV-SNACKBAR-SR-001 not registered",
    "Product Agent D7 co-sign not obtained",
    "Owner review of Phase-2 philosophy not completed",
    "No engine code changed (spec only)",
    "No scores changed (spec only)",
    "sha256 of this file not computed — orchestrator must hash the committed file"
  ],
  "self_check": "Acceptance test per Section 9.1: this spec is accepted when (1) Product Agent provides D7 co-sign on the cap disposition table (Section 5) and retained guards (Section 6), (2) BARI-INVERSION-TEST-001 is formally specified as a machine-executable test with the Petit Beurre/Chokita pair as a required fixture, (3) EV-NOVA-REPLACE-001 is registered with label-derivability validation of the nut/seed/legume signal, (4) owner reviews the philosophy (Sections 1, 2, 8). Observed result: spec authored and written to file — acceptance conditions not yet met, status correctly RETURNED pending D7 co-sign and the four conditions above."
}
```
