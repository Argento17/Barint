# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/crackers_frontend_v1.json`
**Generated:** 2026-07-05T09:03:16Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [FAIL] G2 COVERAGE | FAIL |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #._meta.exclusions[0]: additional property 'dropped_at' not allowed
  FAIL: #._meta.exclusions[0]: additional property 'stage' not allowed
  FAIL: #._meta.exclusions[0]: additional property 'task' not allowed

### [FAIL] G2 COVERAGE
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
  INFO: Corpus barcodes with image in BSIP1: 54/54
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 0/53 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 0/53 authored (53 PENDING)
  FAIL: v3 consumerExplanation.whyRated: 53/53 products still PENDING_COPY
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 0/53 authored (53 PENDING)
  FAIL: v3 bestUseCases: 53/53 products still PENDING_COPY

### [PASS] G3 SCOPE
  INFO: Displayed products: 53
  INFO: Scored products (trace dirs): 54
  INFO: Declared exclusions in _meta: 1
  INFO:   missing barcode 7290112968807: excluded — insufficient_data: unrecoverable per-serving/per-100g nutrition corruption, discard-rule. Full nutrition block (kcal/protein/carbs/fiber/sodium) was ~1/4.6 of near-identical sibling 'פיטנס' products with no clean unit/parse scaling factor -> nulled at BSIP1 source (TASK-433 FIX2b, missing-data-discard rule) -> engine returns insufficient_data/neutral score -> a gradeless row does not belong on a comparison page. Same rule as the existing BSIP1-stage discard of 5317200 (total data blackout), applied one stage later because this product's corruption was found and nulled during the TASK-433 rework, not at initial scrape.

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=53 baseline=53
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=568  baseline=568  delta=+0
  INFO: Per-barcode grade changes (13):
  INFO:   barcode=7290018371275 [מיני פריכיות כוסמת]: B -> A
  INFO:   barcode=7290018790328 [קרקר מרובע מלוח]: D -> C
  INFO:   barcode=7290019431794 [פריכיות כוסמת עם קינואה]: B -> A
  INFO:   barcode=7290020179043 [פריכיות כוסמת עם טף]: B -> A
  INFO:   barcode=7290110560300 [פריכיות משולש פלפל שחור]: C -> B
  INFO:   barcode=7290118426516 [פיטנס פריכיות דקות תירס]: C -> B
  INFO:   barcode=7296073343202 [פריכיות כוסמת]: B -> A
  INFO:   barcode=7296073398875 [קרם קרקר]: C -> B
  INFO:   barcode=7296073420323 [פריכיות כוסמת אורגנית]: B -> A
  INFO:   barcode=7296073420330 [פריכיות כוסמת ללא מלח]: B -> A
  INFO:   barcode=74375 [קרקר זהב אסם]: D -> C
  INFO:   barcode=9322969000046 [פריכיות תירס אורגניות]: B -> A
  INFO:   barcode=96086000577 [קרקר כוסמין אורגני]: B -> A
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               53          53          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          568         568          +0
  INFO:   Grade changes                               13           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
