# Bari Page Generator — Gate Report

**Input:** `C:/Bari/_g6_cheese.json`
**Generated:** 2026-06-25T06:06:17Z  |  **Elapsed:** 0.2s

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
| [SKIP] G9 INVERSION-INVARIANT | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[3]: additional property 'brand' not allowed
  FAIL: #.products[4]: additional property 'brand' not allowed
  FAIL: #.products[5]: additional property 'brand' not allowed
  FAIL: #.products[6]: additional property 'brand' not allowed
  FAIL: #.products[7]: additional property 'brand' not allowed
  FAIL: #.products[8]: additional property 'brand' not allowed
  FAIL: #.products[9]: additional property 'brand' not allowed
  FAIL: #.products[10]: additional property 'brand' not allowed
  FAIL: #.products[11]: additional property 'brand' not allowed
  FAIL: #.products[12]: additional property 'brand' not allowed
  FAIL: #.products[13]: additional property 'brand' not allowed
  FAIL: #.products[14]: additional property 'brand' not allowed
  FAIL: #.products[15]: additional property 'brand' not allowed
  FAIL: #.products[16]: additional property 'brand' not allowed
  FAIL: #.products[17]: additional property 'brand' not allowed
  FAIL: #.products[18]: additional property 'brand' not allowed
  FAIL: #.products[19]: additional property 'brand' not allowed
  FAIL: ... and 33 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 53/53 non-null
  INFO: name: 53/53 non-null
  INFO: score: 53/53 non-null
  INFO: grade: 53/53 non-null
  INFO: insightLine: 53/53 non-null
  INFO: expansion: 53/53
  INFO: expansion.ingredients: 48/53
  INFO: expansion.nutrition.energyKcal: 53/53
  INFO: expansion.nutrition.protein: 48/53
  INFO: expansion.nutrition.sugar: 33/53
  INFO: expansion.nutrition.fat: 48/53
  INFO: expansion.nutrition.fiber: 2/53
  INFO: expansion.nutrition.sodium: 53/53
  INFO: expansion.confidenceLabel: 53/53
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 53/53 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 53/53 authored (0 PENDING)
  INFO: v3 bariInterpretation.interpretation: 530/530 authored (0 PENDING)
  INFO: v3 bestUseCases: 53/53 authored (0 PENDING)

### [WARN] G3 SCOPE
  INFO: Displayed products: 53
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290014758681: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6040619: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127077: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127329: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=41445: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290110321277: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=474502: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290010945481: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290102393268: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116934280: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2868996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114311472: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114310918: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4127336: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=41452: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2824183: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2824640: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108506624: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=56272: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931241: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011194246: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3523230065467: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3075850: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116934365: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201798154: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6492852: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108504378: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635369: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014759084: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635376: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119375219: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=554983: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290108502541: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201521493: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=554969: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=554976: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5992889: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453123: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201139278: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116935409: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290014762831: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112342102: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116936604: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635116: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129118: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129101: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4129156: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116931982: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116933078: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290116932644: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011499624: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635581: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019635383: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
