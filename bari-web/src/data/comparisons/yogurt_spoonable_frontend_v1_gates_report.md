# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/yogurt_spoonable_frontend_v1.json`
**Generated:** 2026-07-08T12:26:02Z  |  **Elapsed:** 0.2s

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
  INFO: imageUrl: 78/78 non-null
  INFO: name: 78/78 non-null
  INFO: score: 78/78 non-null
  INFO: grade: 78/78 non-null
  INFO: insightLine: 78/78 non-null
  INFO: expansion: 78/78
  INFO: expansion.ingredients: 78/78
  INFO: expansion.nutrition.energyKcal: 78/78
  INFO: expansion.nutrition.protein: 78/78
  INFO: expansion.nutrition.sugar: 78/78
  INFO: expansion.nutrition.fat: 78/78
  INFO: expansion.nutrition.fiber: 38/78
  INFO: expansion.nutrition.sodium: 78/78
  INFO: expansion.confidenceLabel: 78/78
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 78/78 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 78/78 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 780/780 authored (0 PENDING)
  INFO: v3 bestUseCases: 78/78 authored (0 PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 78
  INFO: Scored products (trace dirs): 94
  INFO: Declared exclusions in _meta: 16
  INFO:   missing barcode 43944: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 45771: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 5416415: excluded — TASK-515 owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 57149: excluded — TASK-515 dedup-drop: byte-identical duplicate of canonical EAN-13 7290014758100 (KEPT).
  INFO:   missing barcode 7290014758117: excluded — TASK-515 dedup-drop (owner ruling): byte-identical duplicate of clean twin 57132 (KEPT); also carried confirmed Class-D diabetes-seal contamination -- dropping removes both the duplicate and the contamination in one action.
  INFO:   missing barcode 7290110321031: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290110328788: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290110329952: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116932484: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116934402: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116935614: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116935621: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936123: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936215: excluded — TASK-515 owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936222: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936581: excluded — TASK-515 owner-directed dump: field unrecoverable across all 4 retailers (rescrape acc0c9ac). Class A source-implausible single-ingredient milk declaration (10.0g/100g protein) -- missing_data_discard_rule.

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
