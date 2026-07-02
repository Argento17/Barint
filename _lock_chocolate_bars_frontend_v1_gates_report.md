# Bari Page Generator — Gate Report

**Input:** `C:/Bari/_lock_chocolate_bars_frontend_v1.json`
**Generated:** 2026-06-25T06:21:14Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |
| [SKIP] G9 INVERSION-INVARIANT | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[0].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[0].d4_additives[0]: additional property 'cosmetic_mup' not allowed
  FAIL: #.products[0]: additional property 'name_he' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[0]: additional property 'image_url' not allowed
  FAIL: #.products[0]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[0]: additional property '_scoring_trace' not allowed
  FAIL: #.products[1].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[1].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[1].d4_additives[0]: additional property 'cosmetic_mup' not allowed
  FAIL: #.products[1].d4_additives[1]: additional property 'cosmetic_mup' not allowed
  FAIL: #.products[1]: additional property 'name_he' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[1]: additional property 'image_url' not allowed
  FAIL: #.products[1]: additional property 'nutrition_per_100g' not allowed
  FAIL: #.products[1]: additional property '_scoring_trace' not allowed
  FAIL: #.products[2].expansion.limitingFactors[0]: expected type string, got dict
  FAIL: #.products[2].expansion.limitingFactors[1]: expected type string, got dict
  FAIL: #.products[2].d4_additives[0]: additional property 'cosmetic_mup' not allowed
  FAIL: ... and 188 more errors

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
  INFO: expansion.nutrition.sugar: 23/23
  INFO: expansion.nutrition.fat: 23/23
  INFO: expansion.nutrition.fiber: 4/23
  INFO: expansion.nutrition.sodium: 23/23
  INFO: expansion.confidenceLabel: 23/23
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 23
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=5000159560511: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72991008: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106651265: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116536781: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116536774: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900951310379: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110571405: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000159559485: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3800020401552: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105362377: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290100249086: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116532011: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116531748: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116532042: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116537375: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112494283: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72917329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72917367: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077617041: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5000159561976: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116534442: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=72918388: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=34000250103: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=5900951310379 field=expansion.comparisonContext: sodium causally framed: 'בגלל הנתרן'
  FAIL: barcode=72917329 field=rowVerdict: banned phrase 'חלבון נמוך' found
  FAIL: barcode=72917329 field=expansion.comparisonContext: banned phrase 'חלבון נמוך' found
  FAIL: barcode=4823077617041 field=insightLine: banned phrase 'חלבון נמוך' found
  FAIL: barcode=4823077617041 field=expansion.comparisonContext: banned phrase 'חלבון נמוך' found
  FAIL: barcode=72918388 field=insightLine: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
