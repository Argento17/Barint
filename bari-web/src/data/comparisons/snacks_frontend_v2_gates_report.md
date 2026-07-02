# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/snacks_frontend_v2.json`
**Generated:** 2026-06-18T15:16:31Z  |  **Elapsed:** 0.1s

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
  FAIL: #.products[0]: additional property '_internal_cluster' not allowed
  FAIL: #.products[1]: additional property '_internal_cluster' not allowed
  FAIL: #.products[2]: additional property '_internal_cluster' not allowed
  FAIL: #.products[3]: additional property '_internal_cluster' not allowed
  FAIL: #.products[4]: additional property '_internal_cluster' not allowed
  FAIL: #.products[5]: additional property '_internal_cluster' not allowed
  FAIL: #.products[6]: additional property '_internal_cluster' not allowed
  FAIL: #.products[7]: additional property '_internal_cluster' not allowed
  FAIL: #.products[8]: additional property '_internal_cluster' not allowed
  FAIL: #.products[9]: additional property '_internal_cluster' not allowed
  FAIL: #.products[10]: additional property '_internal_cluster' not allowed
  FAIL: #.products[11]: additional property '_internal_cluster' not allowed
  FAIL: #.products[12]: additional property '_internal_cluster' not allowed
  FAIL: #.products[13]: additional property '_internal_cluster' not allowed
  FAIL: #.products[14]: additional property '_internal_cluster' not allowed
  FAIL: #.products[15]: additional property '_internal_cluster' not allowed
  FAIL: #.products[16]: additional property '_internal_cluster' not allowed
  FAIL: #.products[17]: additional property '_internal_cluster' not allowed

### [WARN] G2 COVERAGE
  INFO: imageUrl: 18/18 non-null
  INFO: name: 18/18 non-null
  INFO: score: 18/18 non-null
  INFO: grade: 18/18 non-null
  INFO: insightLine: 18/18 non-null
  INFO: expansion: 18/18
  INFO: expansion.ingredients: 0/18
  INFO: expansion.nutrition.energyKcal: 0/18
  INFO: expansion.nutrition.protein: 0/18
  INFO: expansion.nutrition.sugar: 0/18
  INFO: expansion.nutrition.fat: 0/18
  INFO: expansion.nutrition.fiber: 0/18
  INFO: expansion.nutrition.sodium: 0/18
  INFO: expansion.confidenceLabel: 18/18
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 17
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290011498870: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498894: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498948: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207210287: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011498894: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207209885: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610379: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207208260: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610386: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207210928: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000423534: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=16000548404: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207208680: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610492: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410076610508: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5900020039590: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207206495: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8423207207362: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
