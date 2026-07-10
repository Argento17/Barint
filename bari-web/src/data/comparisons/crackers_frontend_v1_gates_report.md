# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\crackers_frontend_v1.json`
**Generated:** 2026-07-10T08:45:07Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
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

### [PASS] G2 COVERAGE
  INFO: imageUrl: 53/53 non-null
  INFO: name: 53/53 non-null
  INFO: score: 53/53 non-null
  INFO: grade: 53/53 non-null
  INFO: insightLine: 53/53 non-null
  INFO: expansion: 53/53
  INFO: expansion.ingredients: 53/53
  INFO: expansion.nutrition.energyKcal: 53/53
  INFO: expansion.nutrition.protein: 53/53
  INFO: expansion.nutrition.sugar: 35/53
  INFO: expansion.nutrition.fat: 53/53
  INFO: expansion.nutrition.fiber: 50/53
  INFO: expansion.nutrition.sodium: 53/53
  INFO: expansion.confidenceLabel: 53/53
  INFO: Corpus barcodes with image in BSIP1: 20/20
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 0/53 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 0/53 authored (0 PENDING, 53 not used by this page)
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 0/53 authored (0 PENDING, 53 not used by this page)

### [WARN] G3 SCOPE
  INFO: Displayed products: 53
  INFO: Scored products (trace dirs): 20
  INFO: Declared exclusions in _meta: 1
  INFO:   missing barcode 7290112968807: excluded — insufficient_data: unrecoverable per-serving/per-100g nutrition corruption, discard-rule. Full nutrition block (kcal/protein/carbs/fiber/sodium) was ~1/4.6 of near-identical sibling 'פיטנס' products with no clean unit/parse scaling factor -> nulled at BSIP1 source (TASK-433 FIX2b, missing-data-discard rule) -> engine returns insufficient_data/neutral score -> a gradeless row does not belong on a comparison page. Same rule as the existing BSIP1-stage discard of 5317200 (total data blackout), applied one stage later because this product's corruption was found and nulled during the TASK-433 rework, not at initial scrape.
  WARN: Displayed barcode 4267230 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 4952792 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290017325422 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290018371275 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019431794 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290020179043 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110560300 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290110560317 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290111564291 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290112340122 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290112348999 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118422129 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118426516 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290118426530 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290119373352 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073079002 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073079019 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073106098 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073151463 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073161479 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073195252 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073195269 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073343202 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073343219 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073420323 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073420330 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073441335 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073450740 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7296073592440 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 8423207208871 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 9322969000015 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 9322969000022 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 9322969000039 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 9322969000046 has no BSIP2 trace in --run dir (ghost product)

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7296073343202: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073420323: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073420330: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019431794: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020179043: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9322969000046: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018371275: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9322969000022: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9322969000015: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073106098: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110560317: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073592440: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017325422: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9322969000039: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073079019: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073195252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073195269: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4952792: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073079002: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073151463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073343219: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073441335: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290111564291: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112340122: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112348999: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073161479: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110560300: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118426530: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118426516: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207208871: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073450740: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119373352: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118422129: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4267230: no trace found in --run dir, cannot verify score vs trace

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
