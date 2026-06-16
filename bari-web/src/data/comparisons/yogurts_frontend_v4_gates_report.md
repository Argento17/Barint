# Bari Page Generator — Gate Report

**Input:** `C:/bari/bari-web/src/data/comparisons/yogurts_frontend_v4.json`
**Generated:** 2026-06-12T13:54:22Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [FAIL] G2 COVERAGE | FAIL |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [PASS] G7 PARITY | PASS |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0].score: expected type ['integer', 'null'], got float
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[0]: additional property '_cluster' not allowed
  FAIL: #.products[1].score: expected type ['integer', 'null'], got float
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[1]: additional property '_cluster' not allowed
  FAIL: #.products[2].score: expected type ['integer', 'null'], got float
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[2]: additional property '_cluster' not allowed
  FAIL: #.products[3].score: expected type ['integer', 'null'], got float
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[3]: additional property 'brand' not allowed
  FAIL: #.products[3]: additional property '_cluster' not allowed
  FAIL: ... and 61 more errors

### [FAIL] G2 COVERAGE
  INFO: imageUrl: 11/17 non-null
  INFO: name: 17/17 non-null
  INFO: score: 17/17 non-null
  INFO: grade: 17/17 non-null
  INFO: insightLine: 17/17 non-null
  INFO: expansion: 17/17
  INFO: expansion.ingredients: 0/17
  INFO: expansion.nutrition.energyKcal: 17/17
  INFO: expansion.nutrition.protein: 17/17
  INFO: expansion.nutrition.sugar: 14/17
  INFO: expansion.nutrition.fat: 17/17
  INFO: expansion.nutrition.fiber: 3/17
  INFO: expansion.nutrition.sodium: 17/17
  INFO: expansion.confidenceLabel: 17/17
  INFO: Corpus barcodes with image in BSIP1: 88/88
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290110565527
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290112330352
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290116934402
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290110328764
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290102394081
  FAIL: imageUrl missing in frontend but BSIP1 has image: barcode 7290102399819
  INFO: name: all products have Hebrew characters in name

### [FAIL] G3 SCOPE
  INFO: Displayed products: 17
  INFO: Scored products (trace dirs): 87
  INFO: Declared exclusions in _meta: 1
  INFO:   missing barcode 408316: mentioned in provenance string (treat as explained)
  FAIL: Scored barcode 2824466 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 3126712 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 408354 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4119133 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 43944 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 45771 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 4584528 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5416262 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5416415 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 57132 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 57149 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5839078 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 6664990 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014890572 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290016606522 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017065588 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290019635819 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102390427 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102390465 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102390489 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102391844 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393039 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393060 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393169 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393176 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393190 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102393947 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102395231 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102396740 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102397600 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102397617 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102399635 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290102399802 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110321697 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110321703 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110323585 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110323592 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110328627 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110328788 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110329952 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110558284 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110558314 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110566975 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290110578053 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112330390 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112346629 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114310406 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114311359 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114312424 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114312431 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114313070 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114313377 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114314053 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114314060 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290114314596 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290115678222 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116932484 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116935614 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116935621 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116936123 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116936215 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116936222 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119370177 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119370955 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119372997 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119377404 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119377411 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119377480 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290119380916 not in frontend and not explained in _meta exclusions

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=7290110321031 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290116934402 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found
  FAIL: barcode=7290110328764 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found
  FAIL: barcode=7290110321680 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found
  FAIL: barcode=7290102394081 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found
  FAIL: barcode=7290102399819 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found
  FAIL: barcode=7290010471669 field=expansion.limitingFactors[0]: banned phrase 'מוצר מעובד מאוד' found

### [PASS] G7 PARITY
  INFO: Product count: current=17 baseline=19
  INFO: Products removed vs baseline (1): 7290000408316
  INFO: Image coverage: current=64.7%  baseline=94.7%  delta=-30.0%
  INFO: Avg consumer-text chars/product: current=282  baseline=229  delta=+53
  INFO: Per-barcode grade changes (8):
  INFO:   barcode=7290014758100 [יוגורט ביו תנובה 3%]: A -> B
  INFO:   barcode=7290014758117 [יוגורט ביו תנובה 1.5%]: A -> B
  INFO:   barcode=7290102399819 [מולר פרוטאין יוגורט פירות יער]: B -> D
  INFO:   barcode=7290110328221 [יוגורט נטול לקטוז 3% שומן]: A -> B
  INFO:   barcode=7290110328764 [יוגורט GO קרמי תות]: B -> C
  INFO:   barcode=7290110565527 [דנונה PRO 20 גרם חלבון]: A -> S
  INFO:   barcode=7290112336712 [דנונה פרו 21 חלבון 0%]: A -> S
  INFO:   barcode=7290116934402 [יוגורט אוורירי GO מנגו]: B -> C
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               17          19          -2
  INFO:   Image coverage %                          64.7        94.7       -30.0
  INFO:   Avg chars/product                          282         229         +53
  INFO:   Grade changes                                8           —           —
  INFO:   Products added                               0           —           —
  INFO:   Products removed                             1           —           —
