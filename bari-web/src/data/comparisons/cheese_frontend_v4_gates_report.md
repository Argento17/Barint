# Bari Page Generator — Gate Report

**Input:** `C:\Bari\bari-web\src\data\comparisons\cheese_frontend_v4.json`
**Generated:** 2026-07-01T15:25:54Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [PASS] G2 COVERAGE | PASS |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

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
  FAIL: ... and 27 more errors

### [PASS] G2 COVERAGE
  INFO: imageUrl: 47/47 non-null
  INFO: name: 47/47 non-null
  INFO: score: 47/47 non-null
  INFO: grade: 47/47 non-null
  INFO: insightLine: 47/47 non-null
  INFO: expansion: 47/47
  INFO: expansion.ingredients: 47/47
  INFO: expansion.nutrition.energyKcal: 47/47
  INFO: expansion.nutrition.protein: 47/47
  INFO: expansion.nutrition.sugar: 28/47
  INFO: expansion.nutrition.fat: 47/47
  INFO: expansion.nutrition.fiber: 2/47
  INFO: expansion.nutrition.sodium: 47/47
  INFO: expansion.confidenceLabel: 47/47
  INFO: Corpus barcodes with image in BSIP1: 59/59
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [PASS] G3 SCOPE
  INFO: Displayed products: 47
  INFO: Scored products (trace dirs): 47
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  FAIL: barcode=7290014758681: JSON score=86.6 vs trace score=89.8 (diff=3.200 > tolerance=0.05)
  FAIL: barcode=6040619: JSON score=81.2 vs trace score=82.6 (diff=1.400 > tolerance=0.05)
  FAIL: barcode=4127077: JSON score=79.7 vs trace score=88.8 (diff=9.100 > tolerance=0.05)
  FAIL: barcode=4127329: JSON score=77.9 vs trace score=87.0 (diff=9.100 > tolerance=0.05)
  FAIL: barcode=41445: JSON score=77.9 vs trace score=87.0 (diff=9.100 > tolerance=0.05)
  FAIL: barcode=7290110321277: JSON score=77.9 vs trace score=87.0 (diff=9.100 > tolerance=0.05)
  FAIL: barcode=474502: JSON score=75.7 vs trace score=78.9 (diff=3.200 > tolerance=0.05)
  FAIL: barcode=7290010945481: JSON score=75.7 vs trace score=78.9 (diff=3.200 > tolerance=0.05)
  FAIL: barcode=7290102393268: JSON score=75.7 vs trace score=78.9 (diff=3.200 > tolerance=0.05)
  FAIL: barcode=7290116934280: JSON score=74.7 vs trace score=76.1 (diff=1.400 > tolerance=0.05)
  FAIL: barcode=2868996: JSON score=74.5 vs trace score=83.6 (diff=9.100 > tolerance=0.05)
  FAIL: barcode=7290114311472: JSON score=73.5 vs trace score=78.9 (diff=5.400 > tolerance=0.05)
  FAIL: barcode=7290114310918: JSON score=72.5 vs trace score=83.9 (diff=11.400 > tolerance=0.05)
  FAIL: barcode=4127336: JSON score=72.0 vs trace score=81.1 (rounded trace=81, diff=9.000 > tolerance=0.05)
  FAIL: barcode=41452: JSON score=72.0 vs trace score=81.1 (rounded trace=81, diff=9.000 > tolerance=0.05)
  FAIL: barcode=2824183: JSON score=71.6 vs trace score=72.9 (diff=1.300 > tolerance=0.05)
  FAIL: barcode=2824640: JSON score=71.6 vs trace score=72.9 (diff=1.300 > tolerance=0.05)
  FAIL: barcode=56272: JSON score=68.0 vs trace score=69.6 (rounded trace=70, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290116931241: JSON score=67.2 vs trace score=76.4 (diff=9.200 > tolerance=0.05)
  FAIL: barcode=7290011194246: JSON score=66.9 vs trace score=71.5 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=3523230065467: JSON score=63.8 vs trace score=72.3 (diff=8.500 > tolerance=0.05)
  FAIL: barcode=3075850: JSON score=63.7 vs trace score=68.0 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=7290116934365: JSON score=62.0 vs trace score=66.3 (rounded trace=66, diff=4.000 > tolerance=0.05)
  FAIL: barcode=7622201798154: JSON score=60.6 vs trace score=66.0 (diff=5.400 > tolerance=0.05)
  FAIL: barcode=6492852: JSON score=55.7 vs trace score=60.0 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=7290108504378: JSON score=55.4 vs trace score=60.0 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7290019635369: JSON score=54.7 vs trace score=66.1 (diff=11.400 > tolerance=0.05)
  FAIL: barcode=7290014759084: JSON score=53.9 vs trace score=58.2 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=7290019635376: JSON score=51.2 vs trace score=59.9 (diff=8.700 > tolerance=0.05)
  FAIL: barcode=7290119375219: JSON score=50.9 vs trace score=54.8 (diff=3.900 > tolerance=0.05)
  FAIL: barcode=7290108502541: JSON score=47.6 vs trace score=52.0 (diff=4.400 > tolerance=0.05)
  FAIL: barcode=7622201521493: JSON score=47.3 vs trace score=51.9 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7622201139278: JSON score=45.5 vs trace score=47.0 (diff=1.500 > tolerance=0.05)
  FAIL: barcode=7290116935409: JSON score=45.0 vs trace score=54.1 (rounded trace=54, diff=9.000 > tolerance=0.05)
  FAIL: barcode=7290014762831: JSON score=44.8 vs trace score=49.4 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7290112342102: JSON score=44.6 vs trace score=43.5 (diff=1.100 > tolerance=0.05)
  FAIL: barcode=7290116936604: JSON score=44.5 vs trace score=49.1 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7290019635116: JSON score=44.3 vs trace score=52.9 (diff=8.600 > tolerance=0.05)
  FAIL: barcode=4129118: JSON score=43.8 vs trace score=48.2 (diff=4.400 > tolerance=0.05)
  FAIL: barcode=4129101: JSON score=43.1 vs trace score=47.4 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=4129156: JSON score=42.9 vs trace score=47.2 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=7290116931982: JSON score=42.8 vs trace score=47.1 (diff=4.300 > tolerance=0.05)
  FAIL: barcode=7290116933078: JSON score=42.7 vs trace score=47.3 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7290116932644: JSON score=41.7 vs trace score=46.3 (diff=4.600 > tolerance=0.05)
  FAIL: barcode=7290011499624: JSON score=33.6 vs trace score=33.8 (diff=0.200 > tolerance=0.05)
  FAIL: barcode=7290019635581: JSON score=32.8 vs trace score=35.7 (diff=2.900 > tolerance=0.05)
  FAIL: barcode=7290019635383: JSON score=23.2 vs trace score=23.4 (diff=0.200 > tolerance=0.05)

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=7290019635581 field=rowVerdict: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
