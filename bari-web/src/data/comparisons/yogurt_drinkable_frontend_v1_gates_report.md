# Bari Page Generator — Gate Report

**Input:** `C:/bari_wt_yg/bari-web/src/data/comparisons/yogurt_drinkable_frontend_v1.json`
**Generated:** 2026-07-10T06:23:23Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 17/17 non-null
  INFO: name: 17/17 non-null
  INFO: score: 17/17 non-null
  INFO: grade: 17/17 non-null
  INFO: insightLine: 17/17 non-null
  INFO: expansion: 17/17
  INFO: expansion.ingredients: 17/17
  INFO: expansion.nutrition.energyKcal: 17/17
  INFO: expansion.nutrition.protein: 17/17
  INFO: expansion.nutrition.sugar: 17/17
  INFO: expansion.nutrition.fat: 17/17
  INFO: expansion.nutrition.fiber: 7/17
  INFO: expansion.nutrition.sodium: 17/17
  INFO: expansion.confidenceLabel: 17/17
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 0/17 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 0/17 authored (0 PENDING, 17 not used by this page)
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 0/17 authored (0 PENDING, 17 not used by this page)

### [PASS] G3 SCOPE
  INFO: Displayed products: 17
  INFO: Scored products (trace dirs): 25
  INFO: Declared exclusions in _meta: 8
  INFO:   missing barcode 55329: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster yoplait_drink; kept representative 55336). Scored but not displayed.
  INFO:   missing barcode 55343: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster yoplait_drink; kept representative 55336). Scored but not displayed.
  INFO:   missing barcode 6664655: excluded — TASK-515 dedup-drop (unchanged from HIGH-2 ruling): אקטימל לבן מארז -- byte-identical duplicate SKU of barcode 7290119380923 (KEPT, canonical EAN-13).
  INFO:   missing barcode 7290102031276: excluded — TASK-546 near-duplicate cull: pack/flavor variant of same line (cluster actimel_pack; kept representative 7290119380923). Scored but not displayed.
  INFO:   missing barcode 7290105364678: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster activia_drink; kept representative 7290107937542). Scored but not displayed.
  INFO:   missing barcode 7290107938396: excluded — TASK-546 near-duplicate cull: pack/flavor variant of same line (cluster actimel_pack; kept representative 7290119380923). Scored but not displayed.
  INFO:   missing barcode 7290116932774: excluded — TASK-515 owner-directed dump (superseding the prior HIGH-1 discard ruling): גו בננה-קרמל -- fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac), not just this retailer panel. missing_data_discard_rule.
  INFO:   missing barcode 7290116934228: excluded — TASK-515 owner-directed dump (superseding the prior HIGH-1 discard ruling): משקה יוגורט גו מלון תות -- sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac), not just this retailer panel. missing_data_discard_rule.

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
