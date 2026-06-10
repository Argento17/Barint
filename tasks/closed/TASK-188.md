---
id: TASK-188
title: "Confidence-architecture rule: should an A-grade require ingredient observability? (from the 81.2/A granola artifact)"
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
completed_at: 2026-06-05
cc_reviewed: "2026-06-05"
depends_on: [TASK-184]
blocks: []
category_id: null
close_reason: >-
  CC close-readiness gate PASS (2026-06-05). Full ruling+co-sign+implementation chain verified:
  (1) Product ruling: YES conditional — A-grade requires ingredient list observed + additive
  observability confirmed + four core fields non-null; cap 75/B on failure. (2) Nutrition
  co-sign: YES — three conditions correct; Condition 3 must check field values not band labels
  (naming divergence between confidence layers). (3) Implementation: grade_governance.py at
  03_operations/bsip2/proto_v0/src/ (canonical) + _shared re-export. Guard wired into
  cheese/hummus/glassbox_w4/cereals builders; maadanim/bread/yogurt pre-existing. 4-case spot
  check PASS (C1 fail→75/B, all pass→A unchanged, C3 null carbs→75/B, B unchanged).
  Flag BARI_A_GRADE_INGREDIENT_FLOOR default ON. Long-term home: D6 confidence (Glass Box
  TASK-179). Existing published JSONs unaffected until next re-run (by design).
summary: >
  Nutrition flagged (TASK-184 sign-off) that a Carrefour protein-granola hit 81.2/A only because its OFF panel had a sodium cell filled in — giving it a 'medium' confidence band that escaped the 75-cap, while two identical siblings (sodium cell blank -> 'low' band) were capped to 75/B. An A turned on a data-completeness artifact, not nutrition. PROPOSAL for Product/D7: an A-grade (the highest public claim) should require ingredient observability / a minimum confidence floor. Evaluate + co-sign before any rule change. Engine NOT to change without this sign-off. Born from the TASK-140 lesson (don't let a data artifact crown a #1).
---

# TASK-188 — Confidence-architecture rule: should an A-grade require ingredient observability? (from the 81.2/A granola artifact)

## Product Ruling (2026-06-05)

**Ruling: YES — conditional.**

An A-grade requires a minimum ingredient observability floor. A product with `data_sufficiency: insufficient` on additive/ingredient signals cannot reach A regardless of its nutrition score.

### The exact rule

**A-grade ingredient floor (BARI_A_GRADE_INGREDIENT_FLOOR):**

A product may only reach grade A if it satisfies ALL of the following conditions:

1. **Ingredient list observed.** The product must have an ingredient list sourced from at least one of: scraped label (BSIP0), OFF verified panel, or manual enrichment. A product with no ingredient list on record fails this condition.
2. **Additive observability confirmed.** The engine must have made an active determination on additive signals — either no additives found, or additives found and penalized. A product where additive signals were not evaluable (e.g., ingredient list null or unparseable) fails this condition.
3. **Confidence band must be `medium` or `high`.** A product in the `low` confidence band (data_sufficiency: insufficient on key nutritional fields) cannot reach A. The relevant fields for the floor check are: energy_kcal, protein_g, fat_g, carbohydrates_g. If any of these four is null or imputed, the product is in `low` band and capped.

**Cap on failure:** A product that fails any of the three conditions above is capped at **75/B** — not lower, because the nutrition signal may legitimately be strong. The cap is a ceiling on the grade, not a penalty on the score. Score is reported as-is; grade is held at B.

**Scope of this rule:** Applies to all categories. It does not add category-specific exceptions. The 75/B cap mirrors the existing behaviour that triggered this review — the artifact was not that the cap existed but that the confidence band was gamed by a single filled sodium cell when ingredient observability was still absent.

### Why YES

The A grade is Bari's highest public claim. Consumers read it as a full endorsement. If the engine cannot observe what is in the product — the ingredient list, what additives are present — it has no basis to issue that endorsement. A sodium panel being filled in is not the same as ingredient observability. The 81.2/A granola case illustrates the exact failure mode: a data-completeness artifact elevated a product above its information-complete siblings. That is the opposite of what the confidence architecture is supposed to do.

The current confidence-band system (D6 in Glass Box) is the correct long-term home for this logic, but it does not yet exist in the engine. A near-term guard is warranted. The rule above is intentionally narrow: it targets the A-grade ceiling only, leaves all sub-A grading untouched, and does not introduce new penalties.

### What this does NOT do

- Does not change scores. A product that would have scored 81 still scores 81 in the output — it just cannot be graded A.
- Does not block B, C, D, E grades from products with insufficient data. Those grades are already carrying the information that the product is imperfectly observed.
- Does not create a new confidence dimension or score modifier. This is a grade-ceiling guard only.
- Does not retroactively re-grade all published products. It applies at the JSON generation layer before any new category ships and at re-run time for existing categories.

### Where it lives

**Near-term: frontend JSON generation layer.**

The rule is enforced in `build_frontend_json.py` (or equivalent per-category builder script) at the grade-assignment step, after the engine score is computed. The engine score is untouched. The builder checks the three conditions above; if any fails, it writes `grade: B` and caps `score` at 75 before writing the frontend JSON. This requires no flag, no engine change, and no BSIP2 re-run for categories already scored.

**Long-term home: D6 confidence dimension (Glass Box, TASK-179).**

When D6 is built, this logic migrates into the engine as a proper confidence gate. The frontend-layer guard is explicitly a bridge. Once D6 ships, the builder-layer override is removed.

**Flag requirement:** The near-term implementation should be toggled by `BARI_A_GRADE_INGREDIENT_FLOOR=true` in the builder environment so it can be verified against existing category outputs before becoming the default. The flag defaults to ON for all new category builds. It is applied to existing categories at next re-run.

### D7 co-sign requirement

This ruling is Product's sign-off. Nutrition Agent must independently confirm that the three field conditions (energy, protein, fat, carbs as the `low`-band trigger) correctly represent the cases where ingredient observability is genuinely absent and an A is not defensible. Nutrition co-sign is required before engine or builder implementation begins.

### Effect on the granola artifact

The Carrefour protein-granola (81.2/A) would have been capped at 75/B under this rule, matching its information-incomplete siblings. That is the correct outcome.

## Nutrition Co-sign (2026-06-05)

**Co-sign: YES — with one clarification on Condition 3 and one implementation boundary note.**

### Verdict on the three conditions

The three-condition structure is scientifically sound and correctly targets the failure mode. Each condition addresses a distinct, independently meaningful observability gap.

**Condition 1 (ingredient list observed)** is the load-bearing condition. Without an ingredient list, the engine cannot evaluate additive load, ingredient quality, processing signals, or NOVA classification. A product can have a perfect nutrition panel — low sugar, reasonable fat, solid protein — and still contain six emulsifiers, maltodextrin, and flavour compounds. Without the ingredient list those signals are invisible. Awarding A to such a product is not caution; it is a false endorsement. The -25 confidence penalty for missing ingredient list in `compute_confidence()` is not sufficient protection: a product with a full nutrition panel and no ingredient list exits `compute_confidence()` with a score of 75 (100 - 25), which places it in the `high` confidence band. The band ceilings for `high` are `None` — no ceiling, no grade cap. That product can reach A on pure nutrition today. Condition 1 closes that gap correctly.

**Condition 2 (additive observability confirmed)** is logically redundant with Condition 1 for any product where the ingredient list is genuinely absent — if there is no ingredient list, additive evaluation is also not evaluable. Its value is in the partially-observed case: a product where an ingredient list exists but was flagged `ingredient_text_quality: corrupted` or `malformed` such that additive parsing was skipped. In that case Condition 1 passes (list is technically present) but Condition 2 catches the skipped evaluation. This is the correct distinction to maintain. Keep Condition 2 as specified.

**Condition 3 (confidence band medium or high — all four core fields non-null)** is necessary and sufficient for what it is designed to catch. The engine deducts 10 points per missing core macro (energy, protein, fat, carbohydrates). A single missing field leaves confidence at 90 - 10 = 90 before any other deductions, still solidly in `high` band. Two missing fields bring it to 80, still `high`. Only when three or more of the four core fields are missing does the product reliably enter `medium` band (≥60 score) rather than `high`. This means the four-field test as written is not a sufficient proxy for `low` band on its own — a product could fail one or two of these fields and still be `high` band, but the nutrition score would typically be too impaired to reach 80/A anyway (missing energy and protein makes the calorie density and protein quality dimensions score neutrally, which suppresses the total). So Condition 3 operates correctly in practice as belt-and-suspenders against edge cases where the band logic does not fully catch the degraded state.

**One clarification on Condition 3:** The rule text states "If any of these four is null or imputed, the product is in `low` band and capped." This is descriptively inaccurate — one null field does not necessarily produce `low` band. The implementation should not check the band label directly (which can be `high` even with one null field); it should check the four field values themselves. The correct implementation logic is: `if any(product[f] is None for f in [energy_kcal, protein_g, fat_g, carbohydrates_g]): cap at B`. The band label should not be used as the trigger because it conflates multiple confidence deductions. The intent of the condition is correct; the band framing in the prose is a loose description, not an implementable check. The Data Agent should implement the field-level null check, not a band-label check.

### Is 75/B the right cap?

Yes. A product with no ingredient list can still have legitimate nutritional architecture — a single-ingredient whole food (plain yogurt, eggs, olive oil) may have no additive load at all, and its nutrition panel is fully observed. The 75/B cap correctly honours that signal without granting the highest endorsement. It says: "the nutrition we can see looks reasonable, but we cannot confirm what is not shown." That framing is accurate and fair. A product that genuinely has no additives and excellent nutrition will reach A once its ingredient list is confirmed — the rule is not a permanent penalty, it is a floor for what counts as a full endorsement.

Setting the cap lower (e.g. 70/C) would penalize legitimate products too aggressively. Leaving it at exactly 75 is right because that is already the existing `low`-band ceiling in the engine (`CONFIDENCE_LOW_CEILING = 75`), so the builder-layer guard is consistent with the engine's own confidence architecture rather than introducing a new arbitrary threshold.

### Edge cases for implementation

1. **Single-ingredient products (e.g. pure olive oil, whole milk, plain oats).** An ingredients_list of `["שמן זית"]` satisfies Condition 1 — one-element lists are valid. The builder must not apply a minimum length check. The field should be null-checked, not length-checked.

2. **Manually enriched products.** A product can reach A if it has been manually enriched with an ingredient list, even if BSIP0 did not scrape one. Manual enrichment counts as an observed source. The builder should check the field value, not the source of that value.

3. **Ingredient list present but empty string.** `ingredients_list: []` (empty array) or `ingredients_text_he: ""` (empty string) with no items should fail Condition 1. An empty list is not an observed ingredient list. The builder should treat both null and empty as failing.

4. **The `ingredient_text_quality: corrupted` or `malformed` case.** Condition 2 is the correct catch here. If the engine skipped additive evaluation due to parse failure, even with a non-null ingredient list, Condition 2 fails and the cap applies. The builder needs access to the engine's additive evaluation status, not just whether the list field is populated.

5. **Confidence band terminology mismatch.** The rule references `medium or high` bands. The engine's `compute_confidence()` uses `high`, `medium`, `low`, `insufficient` as band names. The `interpretation_confidence.py` layer uses `very_high`, `high`, `moderate`, `low`, `insufficient_context`. The builder must be explicit about which band it reads. For Condition 3, the implementation should bypass band-label logic entirely and check the four field values directly (see clarification above). This avoids any naming mismatch between the two confidence layers.

### Boundary: what this rule does not cover

This rule does not address the case where a product has a formally present but substantively incomplete ingredient list — e.g. a list that was truncated mid-parse, or a list that contains only packaging materials or allergen statements and no actual food ingredients. Those cases are out of scope for this rule and belong to the D4/D6 Glass Box work. The builder-layer guard is a binary floor check on observability, not a quality assessment of what was observed.

### Co-sign record

- Reviewer: Nutrition Agent
- Date: 2026-06-05
- Ruling: YES — confirmed with clarification that Condition 3 must be implemented as a four-field null check, not a band-label check
- D7 co-sign status: APPROVED for builder-layer implementation

---

## Return block

- Deliverable complete: Product ruling written, exact rule specified, implementation layer identified. Nutrition D7 co-sign complete.
- Next owner: Data Agent — implement builder-layer cap per the three conditions and the Condition 3 null-check clarification above.
- After implementation: CC verifies builder output against known artifact (granola Carrefour protein product → must resolve to 75/B, not A) before closing.
- No engine change required.
- No re-runs required before implementation.

---

## Implementation Return Block (Data Agent, 2026-06-05)

**Status: Implementation complete. Returning for CC verification gate.**

### Canonical module

`C:\Bari\03_operations\bsip2\proto_v0\src\grade_governance.py` — the full implementation of `apply_a_grade_floor`. Three conditions (C1 ingredient observed, C2 additive observability, C3 four core fields non-null) exactly as specified by the Product ruling and Nutrition co-sign clarification. Flag `BARI_A_GRADE_INGREDIENT_FLOOR` defaults ON.

`C:\Bari\03_operations\bsip0\scrape\_shared\grade_governance.py` — re-export shim at the task-specified path; adds the bsip2 src path and re-exports `apply_a_grade_floor` and `floor_reasons`.

### Builders wired

| Builder | File | Condition notes |
|---|---|---|
| maadanim | `02_products/maadanim/build_frontend_json.py` | C1: ing text from BSIP1; C2: full trace passed; C3: L1_observed_signals |
| bread | `02_products/bread_retail_003/build_lechem_frontend_json.py` | C1: ing from BSIP0; C2: trace=None (flat format); C3: flat nutrition dict |
| yogurt | `02_products/yogurt_system/build_yogurts_frontend_v2.py` | C1: ing=None (OCR-polluted, withheld by design — all A products cap correctly); C3: L1 signals |
| cheese | `02_products/cheese_spreads/factory_run_004/build_cheese_frontend_v2.py` | Applied AFTER EV-021 cheese gate; C1: ing=None (not yet wired); C3: package nutrition dict |
| hummus | `02_products/hummus/frontend/build_hummus_frontend_v1.py` | C1: ing from BSIP1 ingredients_text_he; C3: BSIP1 normalized_nutrition_per_100g |
| glassbox W4 | `02_products/build_glassbox_w4_frontend.py` | Applied in both build_new_json and build_new_json_delta; C1/C3 from expansion VM; trace=None |
| cereals/granola | `03_operations/bsip2/proto_v0/src/build_cereals_004_frontend.py` | C1: ingredients_text_he from BSIP1; C3: normalized_nutrition_per_100g |

### Condition 3 implementation note

Condition 3 checks the four field values directly as required by the Nutrition co-sign clarification. `_condition3_core_nutrition_non_null` handles three dict shapes (BSIP1/trace keys, BSIP1 normalized keys, VM camelCase keys) so all callers can pass whatever dict they have without transformation.

### CC verification target

The Carrefour protein-granola artifact (81.2/A, granola category, TASK-184) would fail C1 (no ingredient list observed in OFF feed at the time) or C3 (sodium cell filled but one of the four core fields absent). On next cereals/granola re-run it must resolve to ≤75/B.

### Files changed

1. `C:\Bari\03_operations\bsip0\scrape\_shared\grade_governance.py` — NEW (re-export shim)
2. `C:\Bari\02_products\cheese_spreads\factory_run_004\build_cheese_frontend_v2.py` — import + call added
3. `C:\Bari\02_products\hummus\frontend\build_hummus_frontend_v1.py` — import + call added
4. `C:\Bari\02_products\build_glassbox_w4_frontend.py` — import + call added (both builder paths)
5. `C:\Bari\03_operations\bsip2\proto_v0\src\build_cereals_004_frontend.py` — import + call added
6. `C:\Bari\tasks\TASK-188.md` — this return block

Previously wired (not changed here — already complete from prior attempt):
- `C:\Bari\03_operations\bsip2\proto_v0\src\grade_governance.py` (canonical implementation)
- `C:\Bari\02_products\maadanim\build_frontend_json.py`
- `C:\Bari\02_products\bread_retail_003\build_lechem_frontend_json.py`
- `C:\Bari\02_products\yogurt_system\build_yogurts_frontend_v2.py`
