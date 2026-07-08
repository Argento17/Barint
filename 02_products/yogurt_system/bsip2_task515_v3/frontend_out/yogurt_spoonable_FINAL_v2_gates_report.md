# Bari Page Generator — Gate Report

**Input:** `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_spoonable_FINAL_v2.json`
**Generated:** 2026-07-05T15:23:26Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 74/78 non-null
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

### [WARN] G3 SCOPE
  INFO: Displayed products: 78
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290112336712: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110565527: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114311069: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4068011: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110558284: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102395224: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4584528: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6664990: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102395231: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=57132: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014758100: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5839078: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110561352: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110328221: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=408316: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112341686: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110573713: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115678222: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107936309: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016606522: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014890589: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290012645297: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014890572: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107958035: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4119133: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017065588: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110566975: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112330352: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112330390: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119377411: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3126712: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119386642: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4068172: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114314596: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119370177: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119370955: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119372997: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119384242: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119377404: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110323592: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112346797: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110323585: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110328627: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110328764: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114310536: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110321697: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110321680: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102397600: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110321703: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110578053: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102399802: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102399819: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119380916: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102397617: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102394081: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110578572: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6664693: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112346629: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393169: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=408354: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393176: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393947: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114314053: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393039: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393060: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114314060: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114310406: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102390427: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114311359: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102390489: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102391844: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114312424: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290010471669: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114314503: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114312431: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102390465: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102399635: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114313070: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
