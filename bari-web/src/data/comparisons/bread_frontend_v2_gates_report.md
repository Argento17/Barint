# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/bread_frontend_v2.json`
**Generated:** 2026-06-18T15:16:27Z  |  **Elapsed:** 0.0s

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
  FAIL: #.products[0].barcode: expected type string, got NoneType
  FAIL: #.products[1].barcode: expected type string, got NoneType
  FAIL: #.products[2].barcode: expected type string, got NoneType
  FAIL: #.products[3].barcode: expected type string, got NoneType
  FAIL: #.products[4].barcode: expected type string, got NoneType
  FAIL: #.products[5].barcode: expected type string, got NoneType
  FAIL: #.products[8].barcode: expected type string, got NoneType
  FAIL: #.products[9].barcode: expected type string, got NoneType
  FAIL: #.products[10].barcode: expected type string, got NoneType
  FAIL: #.products[11].barcode: expected type string, got NoneType
  FAIL: #.products[12].barcode: expected type string, got NoneType
  FAIL: #.products[15].barcode: expected type string, got NoneType
  FAIL: #.products[16].barcode: expected type string, got NoneType
  FAIL: #.products[17].barcode: expected type string, got NoneType
  FAIL: #.products[18].barcode: expected type string, got NoneType

### [WARN] G2 COVERAGE
  INFO: imageUrl: 19/19 non-null
  INFO: name: 19/19 non-null
  INFO: score: 19/19 non-null
  INFO: grade: 19/19 non-null
  INFO: insightLine: 19/19 non-null
  INFO: expansion: 19/19
  INFO: expansion.ingredients: 4/19
  INFO: expansion.nutrition.energyKcal: 0/19
  INFO: expansion.nutrition.protein: 19/19
  INFO: expansion.nutrition.sugar: 0/19
  INFO: expansion.nutrition.fat: 0/19
  INFO: expansion.nutrition.fiber: 19/19
  INFO: expansion.nutrition.sodium: 19/19
  INFO: expansion.confidenceLabel: 19/19
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 19
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=2079996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=497044: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268429: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481203: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3268252: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=574370: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016245325: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500316: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079033: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3054183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=481197: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079927: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079477: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016967074: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018500460: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4685027: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451507: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6451484: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2079217: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
