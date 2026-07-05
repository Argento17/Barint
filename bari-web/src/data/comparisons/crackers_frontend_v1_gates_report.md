# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/crackers_frontend_v1.json`
**Generated:** 2026-07-05T08:03:03Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [FAIL] G2 COVERAGE | FAIL |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

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
  INFO: Product count: current=53 baseline=19
  INFO: Products added vs baseline (34): 4267230, 4952792, 7290017325422, 7290018371275, 7290019431794, 7290020179043, 7290110560300, 7290110560317, 7290111564291, 7290112340122, 7290112348999, 7290118422129, 7290118426516, 7290118426530, 7290119373352, 7296073079002, 7296073079019, 7296073106098, 7296073151463, 7296073161479, 7296073195252, 7296073195269, 7296073343202, 7296073343219, 7296073420323, 7296073420330, 7296073441335, 7296073450740, 7296073592440, 8423207208871, 9322969000015, 9322969000022, 9322969000039, 9322969000046
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=568  baseline=484  delta=+83
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               53          19         +34
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          568         484         +83
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                              34           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
