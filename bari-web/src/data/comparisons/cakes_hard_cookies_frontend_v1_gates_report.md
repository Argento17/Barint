# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\cakes_hard_cookies_frontend_v1.json`
**Generated:** 2026-07-10T08:45:04Z  |  **Elapsed:** 0.8s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [PASS] G2 COVERAGE | PASS |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[3].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[4].expansion: missing required field 'comparisonContext'
  FAIL: #.products[4].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[4].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[5].expansion: missing required field 'comparisonContext'
  FAIL: #.products[5].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[5].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[6].expansion: missing required field 'comparisonContext'
  FAIL: #.products[6].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: ... and 166 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 62/62 non-null
  INFO: name: 62/62 non-null
  INFO: score: 62/62 non-null
  INFO: grade: 62/62 non-null
  INFO: insightLine: 62/62 non-null
  INFO: expansion: 62/62
  INFO: expansion.ingredients: 62/62
  INFO: expansion.nutrition.energyKcal: 62/62
  INFO: expansion.nutrition.protein: 62/62
  INFO: expansion.nutrition.sugar: 62/62
  INFO: expansion.nutrition.fat: 62/62
  INFO: expansion.nutrition.fiber: 11/62
  INFO: expansion.nutrition.sodium: 62/62
  INFO: expansion.confidenceLabel: 62/62
  INFO: Corpus barcodes with image in BSIP1: 167/167
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [FAIL] G3 SCOPE
  INFO: Displayed products: 62
  INFO: Scored products (trace dirs): 149
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 313184 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4006529002170 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4017100198151 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4017100364112 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4504656 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4504670 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 46214731552 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 46214930207 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4820180816552 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4820180816576 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4820180816590 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4823077633317 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5317194 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5410126006049 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5410126116168 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5410126726244 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5410126806250 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5431920 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5901414200411 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290000061245 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290000075143 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290011489625 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013145406 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013156006 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013156921 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013453068 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290013740014 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017724171 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017962139 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290018893036 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019293804 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019816034 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019816058 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019816232 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019870463 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019870470 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290020030184 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290101111986 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290105364784 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106571921 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106571945 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290106656727 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112340276 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112961754 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290115206333 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290118422617 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290118423904 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290118426615 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040513 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040568 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040605 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040612 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040650 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040667 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040803 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119040858 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119041053 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119041107 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119041152 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119043095 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119043149 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119043743 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119043897 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290122781359 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290123330488 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073161981 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073162001 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073453840 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073453857 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073529019 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073529026 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073659969 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622201401900 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622201809188 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622210137234 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622210453327 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622300356767 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622300489427 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7622300489434 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8000500366073 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8410376037784 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8410376075915 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8710502064814 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8710502139017 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8710502279010 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8710502405204 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8710502470028 not in frontend and not explained in _meta exclusions

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=7290119030095: JSON score=50.5 vs trace score=57.0 (diff=6.500 > tolerance=0.05)
  FAIL: barcode=5718021: JSON score=32.2 vs trace score=37.5 (diff=5.300 > tolerance=0.05)
  FAIL: barcode=7290119045013: JSON score=32.0 vs trace score=37.3 (rounded trace=37, diff=5.000 > tolerance=0.05)
  FAIL: barcode=7290016162264: JSON score=32.0 vs trace score=37.3 (rounded trace=37, diff=5.000 > tolerance=0.05)
  FAIL: barcode=5431913: JSON score=28.0 vs trace score=30.6 (rounded trace=31, diff=3.000 > tolerance=0.05)
  FAIL: barcode=9399288: JSON score=25.1 vs trace score=30.6 (diff=5.500 > tolerance=0.05)
  FAIL: barcode=1361207: JSON score=23.8 vs trace score=22.4 (diff=1.400 > tolerance=0.05)
  FAIL: barcode=2472186: JSON score=22.1 vs trace score=21.8 (diff=0.300 > tolerance=0.05)
  FAIL: barcode=5718038: JSON score=21.5 vs trace score=21.6 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=4504649: JSON score=20.5 vs trace score=20.6 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=7290018893661: JSON score=18.6 vs trace score=17.6 (diff=1.000 > tolerance=0.05)
  FAIL: barcode=4504687: JSON score=18.6 vs trace score=16.9 (diff=1.700 > tolerance=0.05)
  FAIL: barcode=7290111534010: JSON score=18.5 vs trace score=23.2 (diff=4.700 > tolerance=0.05)
  FAIL: barcode=7290006775023: JSON score=17.8 vs trace score=16.9 (diff=0.900 > tolerance=0.05)
  FAIL: barcode=7290016416961: JSON score=17.5 vs trace score=18.0 (diff=0.500 > tolerance=0.05)
  FAIL: barcode=7296073346333: JSON score=16.1 vs trace score=16.0 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=1361177: JSON score=15.9 vs trace score=12.8 (diff=3.100 > tolerance=0.05)
  FAIL: barcode=7290018893487: JSON score=14.0 vs trace score=12.9 (rounded trace=13, diff=1.000 > tolerance=0.05)
  FAIL: barcode=6983794: JSON score=12.0 vs trace score=13.0 (rounded trace=13, diff=1.000 > tolerance=0.05)
  FAIL: barcode=7290123330884: JSON score=11.8 vs trace score=11.7 (diff=0.100 > tolerance=0.05)
  FAIL: barcode=7290105692498: JSON score=11.8 vs trace score=11.1 (diff=0.700 > tolerance=0.05)
  FAIL: barcode=4170097: JSON score=11.7 vs trace score=11.5 (diff=0.200 > tolerance=0.05)
  FAIL: barcode=7296073431817: JSON score=11.4 vs trace score=12.3 (diff=0.900 > tolerance=0.05)
  FAIL: barcode=2472841: JSON score=11.2 vs trace score=10.8 (diff=0.400 > tolerance=0.05)
  FAIL: barcode=7290123330280: JSON score=10.5 vs trace score=10.1 (diff=0.400 > tolerance=0.05)
  FAIL: barcode=7290123330334: JSON score=10.5 vs trace score=10.1 (diff=0.400 > tolerance=0.05)

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
