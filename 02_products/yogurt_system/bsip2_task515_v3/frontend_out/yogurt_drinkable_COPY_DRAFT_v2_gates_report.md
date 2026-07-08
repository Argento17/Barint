# Bari Page Generator — Gate Report

**Input:** `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_drinkable_COPY_DRAFT_v2.json`
**Generated:** 2026-07-05T11:19:33Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 23/23 non-null
  INFO: name: 23/23 non-null
  INFO: score: 23/23 non-null
  INFO: grade: 23/23 non-null
  INFO: insightLine: 23/23 non-null
  INFO: expansion: 23/23
  INFO: expansion.ingredients: 23/23
  INFO: expansion.nutrition.energyKcal: 23/23
  INFO: expansion.nutrition.protein: 23/23
  INFO: expansion.nutrition.sugar: 22/23
  INFO: expansion.nutrition.fat: 22/23
  INFO: expansion.nutrition.fiber: 9/23
  INFO: expansion.nutrition.sodium: 23/23
  INFO: expansion.confidenceLabel: 23/23
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 23/23 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 23/23 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 230/230 authored (0 PENDING)
  INFO: v3 bestUseCases: 23/23 authored (0 PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 23
  INFO: Scored products (trace dirs): 0
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained
  WARN: Displayed barcode 4068035 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 55329 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 55336 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 55343 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 58030 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 6664655 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019635567 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290020711007 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290020711090 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290102031276 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290102393299 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290105364678 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290105965738 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290107937542 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290107938396 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110325114 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110325121 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110552244 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110573737 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290115676051 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290116932774 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290116934228 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119380923 has no BSIP2 trace in --run dir (ghost product)

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290102393299: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4068035: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020711090: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020711007: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110573737: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110552244: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107937542: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105364678: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115676051: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105965738: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635567: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107938396: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110325114: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116932774: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116934228: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6664655: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119380923: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110325121: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102031276: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55343: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55336: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=55329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=58030: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=7290107938396 field=expansion.consumerExplanation.takeaway: banned phrase 'חלבון נמוך' found
  FAIL: barcode=55343 field=consumerTakeaway: banned phrase 'חלבון נמוך' found
  FAIL: barcode=55343 field=expansion.consumerExplanation.takeaway: banned phrase 'חלבון נמוך' found
  FAIL: barcode=55336 field=consumerTakeaway: banned phrase 'חלבון נמוך' found
  FAIL: barcode=58030 field=expansion.consumerExplanation.whyRated: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
