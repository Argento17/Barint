# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v5.json`
**Generated:** 2026-06-26T19:35:21Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[0]: additional property 'name_he' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[0]: additional property 'image_url' not allowed
  FAIL: #.products[0]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[0]: additional property '_scoring_trace' not allowed
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1]: additional property 'name_he' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[1]: additional property 'image_url' not allowed
  FAIL: #.products[1]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[1]: additional property '_scoring_trace' not allowed
  FAIL: #.products[2].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[2]: additional property 'name_he' not allowed
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[2]: additional property 'image_url' not allowed
  FAIL: #.products[2]: additional property 'nutrition_per_100g' not allowed
  FAIL: ... and 156 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 21/21 non-null
  INFO: name: 21/21 non-null
  INFO: score: 21/21 non-null
  INFO: grade: 21/21 non-null
  INFO: insightLine: 21/21 non-null
  INFO: expansion: 21/21
  INFO: expansion.ingredients: 21/21
  INFO: expansion.nutrition.energyKcal: 21/21
  INFO: expansion.nutrition.protein: 21/21
  INFO: expansion.nutrition.sugar: 21/21
  INFO: expansion.nutrition.fat: 21/21
  INFO: expansion.nutrition.fiber: 20/21
  INFO: expansion.nutrition.sodium: 21/21
  INFO: expansion.confidenceLabel: 21/21
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 21
  INFO: Scored products (trace dirs): 51
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 5900020015174 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5900020029669 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5900020034021 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5900020039590 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131050 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131968 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011131975 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013433244 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017516295 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290020398000 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290020398017 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290020398024 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112497994 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112913487 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112915351 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112915382 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116534619 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290117384589 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290117384596 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119371112 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119383153 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119383160 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290121160582 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290121161886 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290121161916 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290121161930 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290121166850 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8410076602251 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8410076610379 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8410076610386 not in frontend and not explained in _meta exclusions

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=7290100659090: JSON score=66.8 vs trace score=66.9 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=6009684861000: JSON score=26.0 vs trace score=30.0 (rounded trace=30, diff=4.000 > tolerance=0.05)
  FAIL: barcode=8423207208703: JSON score=24.4 vs trace score=24.6 (diff=0.200 > tolerance=0.05)

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=21 baseline=21
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=566  baseline=566  delta=+0
  INFO: No grade changes vs baseline
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               21          21          +0
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                          566         566          +0
  INFO:   Grade changes                                0           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             0           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
