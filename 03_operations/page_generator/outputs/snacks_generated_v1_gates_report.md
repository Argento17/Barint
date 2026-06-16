# Bari Page Generator — Gate Report

**Input:** `C:\Bari\03_operations\page_generator\outputs\snacks_generated_v1.json`
**Generated:** 2026-06-12T14:19:12Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [PASS] G2 COVERAGE | PASS |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [PASS] G7 PARITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
  INFO: imageUrl: 48/53 non-null
  INFO: name: 53/53 non-null
  INFO: score: 53/53 non-null
  INFO: grade: 53/53 non-null
  INFO: insightLine: 53/53 non-null
  INFO: expansion: 53/53
  INFO: expansion.ingredients: 49/53
  INFO: expansion.nutrition.energyKcal: 48/53
  INFO: expansion.nutrition.protein: 48/53
  INFO: expansion.nutrition.sugar: 48/53
  INFO: expansion.nutrition.fat: 48/53
  INFO: expansion.nutrition.fiber: 42/53
  INFO: expansion.nutrition.sodium: 46/53
  INFO: expansion.confidenceLabel: 53/53
  INFO: Corpus barcodes with image in BSIP1: 48/53
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name

### [PASS] G3 SCOPE
  INFO: Displayed products: 53
  INFO: Scored products (trace dirs): 53
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=53 baseline=18
  INFO: Products added vs baseline (36): 16000548503, 16000548909, 4011800000349, 4011800528416, 4011800567613, 4011800628512, 4011800629519, 4011800630515, 4011800632519, 4011800633516, 5900020015174, 5900020018908, 5900020020710, 5900020022325, 5900020029669, 5900020034021, 5900020039620, 7290014525290, 7290014525306, 7290018333952, 7290019545545, 7290107646147, 7290107646154, 7290107646826, 7290107947466, 7290107947480, 7290110563851, 7290111936784, 7290111937262, 7290118427858, 7290118427872, 7290118427896, 8410076602251, 8423207206488, 8423207206501, 8423207208703
  INFO: Image coverage: current=90.6%  baseline=100.0%  delta=-9.4%
  INFO: Avg consumer-text chars/product: current=59  baseline=775  delta=-716
  INFO: Per-barcode grade changes (10):
  INFO:   barcode=16000423534 [קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמ]: D -> C
  INFO:   barcode=16000548404 [קראנצ'י חטיף שיבולת שועל עם דבש חמישייה]: D -> C
  INFO:   barcode=5900020039590 [חטיפי דגנים פיטנס קלאסי שישייה]: E -> D
  INFO:   barcode=8410076610508 [נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים וש]: E -> D
  INFO:   barcode=8423207206495 [מרבה סלים דליס שוקולד מריר חדש]: E -> C
  INFO:   barcode=8423207207362 [מרבה סלים דליס שוקולד לבן חדש]: E -> C
  INFO:   barcode=8423207208260 [מרבה סלים דליס שוקולד חלב ללא גלוטן חדש]: D -> C
  INFO:   barcode=8423207208680 [מרבה סלים דליס לילדים עם שוקולד חלב חדש]: D -> C
  INFO:   barcode=8423207210287 [מרבה סלים דליס שוקולד לבן בטעם יוגורט]: C -> B
  INFO:   barcode=8423207210928 [מרבה סלים טופינג אגוזי לוז]: D -> C
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               53          18         +35
  INFO:   Image coverage %                          90.6       100.0        -9.4
  INFO:   Avg chars/product                           59         775        -716
  INFO:   Grade changes                               10           —           —
  INFO:   Products added                              36           —           —
  INFO:   Products removed                             0           —           —
