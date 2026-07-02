# Bari Page Generator — Gate Report

**Input:** `C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\staging_protein_bars_frontend.json`
**Generated:** 2026-06-25T06:28:00Z  |  **Elapsed:** 0.2s

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
| [PASS] G8 DATA-SANITY | PASS |
| [FAIL] G9 INVERSION-INVARIANT | FAIL |

**Overall: FAIL**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [PASS] G2 COVERAGE
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
  INFO: expansion.nutrition.fiber: 32/33
  INFO: expansion.nutrition.sodium: 33/33
  INFO: expansion.confidenceLabel: 33/33
  INFO: Corpus barcodes with image in BSIP1: 33/33
  INFO: imageUrl: no regression vs BSIP1 corpus
  INFO: name: all products have Hebrew characters in name
  INFO: Unauthored-copy check: SKIP (pre-copy generator output)
  INFO: v3 milk-depth coverage checks: SKIP (copy stage not yet run; 33/33 insightLines still PENDING)

### [PASS] G3 SCOPE
  INFO: Displayed products: 33
  INFO: Scored products (trace dirs): 33
  INFO: Declared exclusions in _meta: 0
  INFO: All scored barcodes are displayed or explained

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [PASS] G7 PARITY
  INFO: Product count: current=33 baseline=16
  INFO: Products added vs baseline (19): 7290015130028, 7290015130035, 7290015130042, 7290018043134, 7290018043899, 7290018703076, 7290018703304, 7290018703984, 7290018703991, 7290019310235, 7290019401018, 7290019401049, 7290019401544, 7290019766018, 7290019766025, 7290019766230, 7290112497994, 7290117384572, 7290119371129
  INFO: Products removed vs baseline (2): 7290119383153, 7290119383160
  INFO: Image coverage: current=100.0%  baseline=100.0%  delta=+0.0%
  INFO: Avg consumer-text chars/product: current=24  baseline=624  delta=-600
  INFO: Per-barcode grade changes (9):
  INFO:   barcode=7290112913487 [חטיף חלבון קרם אגוזים]: E -> D
  INFO:   barcode=7290112915351 [חטיף חלבון קרמל מלוח]: E -> D
  INFO:   barcode=7290112915382 [חטיף חלבון שוקולד דובאי]: E -> D
  INFO:   barcode=7290119371112 [חטיף חלבון קרמל ואגוזים]: D -> C
  INFO:   barcode=7290121160582 [חטיף חלבון חמאת בוטנים]: D -> C
  INFO:   barcode=7290121161916 [חטיף חלבון טריפל שוקולד]: D -> C
  INFO:   barcode=7290121161930 [חטיף חלבון טעם בננה טופי]: D -> C
  INFO:   barcode=8410076610379 [נייטשר פרוטאין שוקולד]: D -> C
  INFO:   barcode=8410076610386 [נייטשר פרוטאין קרמל מלוח]: D -> C
  INFO: 
  INFO: === PARITY SUMMARY TABLE ===
  INFO:   Metric                                 Current    Baseline       Delta
  INFO:   Product count                               33          16         +17
  INFO:   Image coverage %                         100.0       100.0        +0.0
  INFO:   Avg chars/product                           24         624        -600
  INFO:   Grade changes                                9           —           —
  INFO:   Products added                              19           —           —
  INFO:   Products removed                             2           —           —

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [FAIL] G9 INVERSION-INVARIANT
  INFO: Loaded 33 BSIP2 trace records from C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\bsip2_products\products
  INFO: Total traces loaded: 33
  INFO: Excluded (null score): 0
  INFO: Excluded (out_of_scope): 0
  INFO: Eligible for inversion check: 33
  INFO: Hard-gate eligible (confidence_band != insufficient): 33
  INFO: Suspected-only (confidence_band == insufficient, logged WARN): 0
  INFO: Total ordered pairs checked (hard): 432
  INFO: Inversion pairs firing (FAIL): 47
  INFO: Non-firing pairs: 385
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290018043134 (אול אין שוק.לבן עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=3.5 [WORSE] | fat_saturated_g: A=9.9 B=6.2 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290018043899 (אול אין בוטנים קרמל) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=3.6 [WORSE] | fat_saturated_g: A=9.9 B=7.9 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290018703076 (אול אין דאבל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=3.4 [WORSE] | fat_saturated_g: A=9.9 B=7.7 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290018703304 (אול אין קרם עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=3.4 [WORSE] | fat_saturated_g: A=9.9 B=6.3 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=3 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290019310235 (אול אין ונילה קראנץ) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=3.3 [WORSE] | fat_saturated_g: A=9.9 B=6.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290019766018 (אול איןחלבון סופט עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=4.0 [WORSE] | fat_saturated_g: A=9.9 B=9.1 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=3 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290117384589 (חטיף חלבון קרמל מלוח) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=2.9 [WORSE] | fat_saturated_g: A=9.9 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290117384596 (חטיף חלבון פאי קינמון) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=2.9 [WORSE] | fat_saturated_g: A=9.9 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=2.4 [WORSE] | fat_saturated_g: A=9.9 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=2.3 [WORSE] | fat_saturated_g: A=9.9 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290015130028 (WIN חטיף חלבון קרם חלב) | score=51.5
    B(lower rank):  id=7290121161930 (חטיף חלבון טעם בננה טופי) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.4 B=2.5 [WORSE] | fat_saturated_g: A=9.9 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019766025 (אול אין סופט פיסטוק) | score=55
    B(lower rank):  id=7290015130035 (WIN חטיף חלבון קרם קרמל) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.6 B=1.7 [WORSE] | fat_saturated_g: A=9.4 B=7.5 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=3 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019766025 (אול אין סופט פיסטוק) | score=55
    B(lower rank):  id=7290015130042 (WIN חטיף חלבון קרם קרמל) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.6 B=2.3 [WORSE] | fat_saturated_g: A=9.4 B=7.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=3 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290015130042 (WIN חטיף חלבון קרם קרמל) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.3 [WORSE] | fat_saturated_g: A=7.4 B=7.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=2 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290015130042 (WIN חטיף חלבון קרם קרמל) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.3 [WORSE] | fat_saturated_g: A=7.1 B=7.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290018043134 (אול אין שוק.לבן עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=3.5 [WORSE] | fat_saturated_g: A=7.4 B=6.2 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290018043134 (אול אין שוק.לבן עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=3.5 [WORSE] | fat_saturated_g: A=7.1 B=6.2 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290018703304 (אול אין קרם עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=3.4 [WORSE] | fat_saturated_g: A=7.4 B=6.3 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=3 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290018703304 (אול אין קרם עוגיות) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=3.4 [WORSE] | fat_saturated_g: A=7.1 B=6.3 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=4 B=3 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019766025 (אול אין סופט פיסטוק) | score=55
    B(lower rank):  id=7290018703984 (עוגיית חלבון שוקולד צ'יפ) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.6 B=2.5 [WORSE] | fat_saturated_g: A=9.4 B=6.8 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=3 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290018703984 (עוגיית חלבון שוקולד צ'יפ) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.5 [WORSE] | fat_saturated_g: A=7.4 B=6.8 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=2 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290018703984 (עוגיית חלבון שוקולד צ'יפ) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.5 [WORSE] | fat_saturated_g: A=7.1 B=6.8 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290018703991 (עוגיית חלבון דאבל שוקולד) | score=54
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=2.5 B=2.4 [WORSE] | fat_saturated_g: A=7.0 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290018703991 (עוגיית חלבון דאבל שוקולד) | score=54
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=2.5 B=2.3 [WORSE] | fat_saturated_g: A=7.0 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290019310235 (אול אין ונילה קראנץ) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=3.3 [WORSE] | fat_saturated_g: A=7.4 B=6.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=3 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290019310235 (אול אין ונילה קראנץ) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=3.3 [WORSE] | fat_saturated_g: A=7.1 B=6.0 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=4 B=3 [WORSE]
    Supporting: additive_marker_count: A=4 B=4 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401018 (חטיף פרוטאין קרם עוגיות) | score=54
    B(lower rank):  id=7290117384589 (חטיף חלבון קרמל מלוח) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.7 B=2.9 [WORSE] | fat_saturated_g: A=5.5 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=6 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401018 (חטיף פרוטאין קרם עוגיות) | score=54
    B(lower rank):  id=7290117384596 (חטיף חלבון פאי קינמון) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.7 B=2.9 [WORSE] | fat_saturated_g: A=5.5 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=6 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401018 (חטיף פרוטאין קרם עוגיות) | score=54
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.7 B=2.4 [WORSE] | fat_saturated_g: A=5.5 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=6 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401018 (חטיף פרוטאין קרם עוגיות) | score=54
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.7 B=2.3 [WORSE] | fat_saturated_g: A=5.5 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=6 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401018 (חטיף פרוטאין קרם עוגיות) | score=54
    B(lower rank):  id=7290121161930 (חטיף חלבון טעם בננה טופי) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.7 B=2.5 [WORSE] | fat_saturated_g: A=5.5 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=6 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401049 (חטיף פרוטאין שוקולד קרמל) | score=54
    B(lower rank):  id=7290117384589 (חטיף חלבון קרמל מלוח) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.6 B=2.9 [WORSE] | fat_saturated_g: A=5.7 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=8 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401049 (חטיף פרוטאין שוקולד קרמל) | score=54
    B(lower rank):  id=7290117384596 (חטיף חלבון פאי קינמון) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.6 B=2.9 [WORSE] | fat_saturated_g: A=5.7 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=8 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401049 (חטיף פרוטאין שוקולד קרמל) | score=54
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.6 B=2.4 [WORSE] | fat_saturated_g: A=5.7 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=8 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401049 (חטיף פרוטאין שוקולד קרמל) | score=54
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.6 B=2.3 [WORSE] | fat_saturated_g: A=5.7 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=8 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019401049 (חטיף פרוטאין שוקולד קרמל) | score=54
    B(lower rank):  id=7290121161930 (חטיף חלבון טעם בננה טופי) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=3.6 B=2.5 [WORSE] | fat_saturated_g: A=5.7 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=8 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=7290019766025 (אול אין סופט פיסטוק) | score=55
    B(lower rank):  id=7290119371112 (חטיף חלבון קרמל ואגוזים) | score=54
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'fat_source_tier']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=4.6 B=3.7 [WORSE] | fat_saturated_g: A=9.4 B=8.2 [WORSE] | red_label_count: A=1 B=1 | fat_source_tier: A=3 B=2 [WORSE]
    Supporting: additive_marker_count: A=4 B=5 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290117384589 (חטיף חלבון קרמל מלוח) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.9 [WORSE] | fat_saturated_g: A=7.4 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290117384589 (חטיף חלבון קרמל מלוח) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.9 [WORSE] | fat_saturated_g: A=7.1 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290117384596 (חטיף חלבון פאי קינמון) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.9 [WORSE] | fat_saturated_g: A=7.4 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290117384596 (חטיף חלבון פאי קינמון) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.9 [WORSE] | fat_saturated_g: A=7.1 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.4 [WORSE] | fat_saturated_g: A=7.4 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290121160582 (חטיף חלבון חמאת בוטנים) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.4 [WORSE] | fat_saturated_g: A=7.1 B=4.8 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.3 [WORSE] | fat_saturated_g: A=7.4 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290121161916 (חטיף חלבון טריפל שוקולד) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.3 [WORSE] | fat_saturated_g: A=7.1 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610379 (נייטשר פרוטאין שוקולד) | score=55
    B(lower rank):  id=7290121161930 (חטיף חלבון טעם בננה טופי) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=17.2 B=2.5 [WORSE] | fat_saturated_g: A=7.4 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=3 B=6 [SUPPORTING — informational only, not used in fire decision]
  FAIL: INVERSION: A(higher-scored) is nutritionally WORSE than B(lower-scored)
    A(higher rank): id=8410076610386 (נייטשר פרוטאין קרמל מלוח) | score=55
    B(lower rank):  id=7290121161930 (חטיף חלבון טעם בננה טופי) | score=50
    A worse on (3 panel signals): ['sugars_g', 'fat_saturated_g', 'red_label_count']
    A better on: (none -- full inversion)
    Panel signal values (A vs B): sugars_g: A=16.1 B=2.5 [WORSE] | fat_saturated_g: A=7.1 B=4.9 [WORSE] | red_label_count: A=1 B=0 [WORSE] | fat_source_tier: A=4 B=4
    Supporting: additive_marker_count: A=4 B=6 [SUPPORTING — informational only, not used in fire decision]
