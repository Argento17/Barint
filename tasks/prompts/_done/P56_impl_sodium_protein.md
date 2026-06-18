# P56 / Implement shelf-relative sodium + dairy-protein reweight (flag-gated) (route: C1-CURSOR)

Spec-complete scoring-engine change. Implement TWO independent, default-OFF flags per the verified
Nutrition design. The DESIGN/judgment is already done — implement it exactly; do not redesign.
Owner-approved 2026-06-13. Do NOT close — propose RETURNED.

## Read first
- Full design: `C:\Bari\02_products\brined_cheeses\reports\sodium_protein_design_v1.md`
- Engine: `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`
- Constants: `C:\Bari\03_operations\bsip2\proto_v0\src\constants.py`
- Existing precedent to mirror: `BARI_GRAD_SODIUM_V1` / EV-055 (graduated sodium), the archetype
  weight pattern (veg_spread / EV-032), EV-054 HP suppression. Find how flags + bands are wired today.

## FLAG 1 — `BARI_SODIUM_SHELF_RELATIVE_V1` (default OFF)
- Activates ONLY when `BARI_GRAD_SODIUM_V1` is ON AND this flag is ON. Scope: archetypes
  `dairy_protein` + `whole_food_fat`.
- At batch-run start, compute `SHELF_SODIUM_MEDIAN_MG` = median sodium across corpus products with a
  valid sodium panel; store it in the run_record. Also compute shelf sodium stdev.
- `SODIUM_SHELF_SURCHARGE_BANDS` keyed on `distance_above_median = max(0, sodium - SHELF_SODIUM_MEDIAN_MG)`:
  (>=600 → -6), (400-599 → -4), (200-399 → -2), (<200 → 0). Below-median → 0 (no reward layer).
- Surcharge ADDS to `SODIUM_LOAD_GENERAL_GRAD`; the combined sodium penalty is capped by a raised
  `SODIUM_FAMILY_BUDGET_BRINED = 16` (vs current 8) for this context only.
- LOW-VARIANCE GUARD: if shelf sodium stdev < 150mg, suppress the surcharge entirely.

## FLAG 2 — `BARI_DAIRY_PROTEIN_REWEIGHT_V1` (default OFF)
- For `dairy_protein` archetype, apply `DAIRY_PROTEIN_WEIGHTS` (sum MUST equal 1.00):
  processing_quality .15, nutrient_density .15, calorie_density .11, glycemic_quality .12,
  protein_quality .14, additive_quality .10, satiety_support .06, fat_quality .08,
  regulatory_quality .05, whole_food_integrity .04.
- Suppress `HP_FAT_SODIUM_COMBO` for `dairy_protein` when sodium <= 400mg AND additive_marker_count == 0.

## Governance
- Add evidence-registry entries `EV-056` (shelf-relative sodium) + `EV-057` (dairy_protein reweight)
  to `03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md`, citing this design doc +
  owner approval 2026-06-13, both flag-gated default-off.

## HARD ACCEPTANCE GATES (run these yourself; paste output)
1. **Default-OFF byte-identity:** with BOTH new flags OFF, re-score the brined corpus → result MUST
   be byte-identical to `run_brined_004` (grade_dist A:12 B:28 C:7 D:1, same scores). Prove it.
2. **Invariant suite:** run `03_operations\bsip2\proto_v0\shadow\engine_invariants.py` (or wherever
   the 342-case suite lives) → 6/6 PASS.
3. **Flag-ON brined re-grade:** with both flags ON, re-score brined → emit the stable flat table
   (barcode,score,grade,binding_caps,nova,fat,sodium,context_flag). Confirm barcode 7290102397334
   (bulgarit-5%, 1550mg) drops from 88/A to ~80-83; report SHELF_SODIUM_MEDIAN_MG and the full new
   grade distribution. Write this run as `run_brined_005`.
- DO NOT touch any other category's scores. DO NOT change defaults. OFF ban absolute.

## Return (machine-readable contract)
Files changed + shas; the 3 gate outputs above (default-off byte-identity diff, invariant pass,
flag-on brined table + median + distribution); confirm both flags default-off; EV-056/057 added.
Do NOT close — propose RETURNED. End with the return contract (`01_framework\operations\return_contract_v1.md`).
