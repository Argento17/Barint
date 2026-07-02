# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json`
**Generated:** 2026-06-21T13:07:17Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[0]: additional property 'name_he' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[0]: additional property 'rank' not allowed
  FAIL: #.products[0]: additional property 'categoryTotal' not allowed
  FAIL: #.products[0]: additional property 'image_url' not allowed
  FAIL: #.products[0]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[0]: additional property '_scoring_trace' not allowed
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1].d4_additives[0]: additional property 'cosmetic_mup' not allowed
  FAIL: #.products[1].d4_additives[1]: additional property 'cosmetic_mup' not allowed
  FAIL: #.products[1]: additional property 'name_he' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[1]: additional property 'rank' not allowed
  FAIL: #.products[1]: additional property 'categoryTotal' not allowed
  FAIL: #.products[1]: additional property 'image_url' not allowed
  FAIL: #.products[1]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[1]: additional property '_scoring_trace' not allowed
  FAIL: ... and 311 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 33/33 non-null
  INFO: name: 33/33 non-null
  INFO: score: 33/33 non-null
  INFO: grade: 33/33 non-null
  INFO: insightLine: 33/33 non-null
  INFO: expansion: 33/33
  INFO: expansion.ingredients: 33/33
  INFO: expansion.nutrition.energyKcal: 33/33
  INFO: expansion.nutrition.protein: 33/33
  INFO: expansion.nutrition.sugar: 33/33
  INFO: expansion.nutrition.fat: 33/33
  INFO: expansion.nutrition.fiber: 23/33
  INFO: expansion.nutrition.sodium: 33/33
  INFO: expansion.confidenceLabel: 33/33
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 33
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7296073382416: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112197467: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920029759: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920023429: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920023368: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920023443: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4000539280740: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119500437: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893609: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112197443: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119500383: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920028363: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105961525: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5941021001674: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073747819: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290107955782: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4000539280726: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7610400075770: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4000417025005: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920023047: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019870043: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019939412: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920028752: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3046920029674: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112331984: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7610008641001: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7614500010617: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110579463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622202257506: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7614500010013: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622202265648: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112914699: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112348548: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
