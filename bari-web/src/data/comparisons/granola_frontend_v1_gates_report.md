# Bari Page Generator — Gate Report

**Input:** `C:/bari/bari-web/src/data/comparisons/granola_frontend_v1.json`
**Generated:** 2026-06-12T13:54:27Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [FAIL] G1 SCHEMA | FAIL |
| [FAIL] G2 COVERAGE | FAIL |
| [FAIL] G3 SCOPE | FAIL |
| [PASS] G4 OFF | PASS |
| [FAIL] G5 GRADE-INTEGRITY | FAIL |
| [FAIL] G6 COPY-SAFETY | FAIL |
| [SKIP] G7 PARITY | SKIP |

**Overall: FAIL**

## Detail

### [FAIL] G1 SCHEMA
  FAIL: #.products[0]: additional property '_subpool' not allowed
  FAIL: #.products[0]: additional property '_isChildrens' not allowed
  FAIL: #.products[0]: additional property '_wholeGrainClaim' not allowed
  FAIL: #.products[0]: additional property 'confidence_level' not allowed
  FAIL: #.products[1]: additional property '_isChildrens' not allowed
  FAIL: #.products[1]: additional property '_subpool' not allowed
  FAIL: #.products[1]: additional property '_wholeGrainClaim' not allowed
  FAIL: #.products[2]: additional property '_isChildrens' not allowed
  FAIL: #.products[2]: additional property '_subpool' not allowed
  FAIL: #.products[2]: additional property '_wholeGrainClaim' not allowed
  FAIL: #.products[3]: additional property '_isChildrens' not allowed
  FAIL: #.products[3]: additional property '_subpool' not allowed
  FAIL: #.products[3]: additional property '_wholeGrainClaim' not allowed
  FAIL: #.products[4]: additional property '_subpool' not allowed
  FAIL: #.products[4]: additional property '_isChildrens' not allowed
  FAIL: #.products[4]: additional property '_wholeGrainClaim' not allowed
  FAIL: #.products[4]: additional property 'confidence_level' not allowed
  FAIL: #.products[5]: additional property '_subpool' not allowed
  FAIL: #.products[5]: additional property '_isChildrens' not allowed
  FAIL: #.products[5]: additional property '_wholeGrainClaim' not allowed
  FAIL: ... and 161 more errors

### [FAIL] G2 COVERAGE
  INFO: imageUrl: 33/42 non-null
  INFO: name: 42/42 non-null
  INFO: score: 42/42 non-null
  INFO: grade: 42/42 non-null
  INFO: insightLine: 42/42 non-null
  INFO: expansion: 42/42
  INFO: expansion.ingredients: 42/42
  INFO: expansion.nutrition.energyKcal: 42/42
  INFO: expansion.nutrition.protein: 42/42
  INFO: expansion.nutrition.sugar: 8/42
  INFO: expansion.nutrition.fat: 42/42
  INFO: expansion.nutrition.fiber: 39/42
  INFO: expansion.nutrition.sodium: 30/42
  INFO: expansion.confidenceLabel: 42/42
  INFO: Corpus barcodes with image in BSIP1: 63/63
  INFO: imageUrl: no regression vs BSIP1 corpus
  FAIL: name has no Hebrew characters: barcode=7290120871069 name='Granola Protein'
  FAIL: name has no Hebrew characters: barcode=7297488099821 name='Sugarless Gluten Free Granola'
  FAIL: name has no Hebrew characters: barcode=5010026515919 name='Mornflake Crispy Muesli Nutty'
  FAIL: name has no Hebrew characters: barcode=5010026521149 name='Crispy Muesli'
  FAIL: name has no Hebrew characters: barcode=3560070826186 name='MUESLI & Co 2 CHOCOLATS & NOISETTES'

### [FAIL] G3 SCOPE
  INFO: Displayed products: 42
  INFO: Scored products (trace dirs): 63
  INFO: Declared exclusions in _meta: 0
  FAIL: Scored barcode 3387390525960 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5010029000061 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5900020012814 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 5900020036407 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290014471443 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290016883176 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017325910 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017894904 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017894911 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290017894928 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290107647731 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290107647854 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112494351 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112495228 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290112495433 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116530482 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290116535371 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7290118420811 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073642022 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073642046 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073705550 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073705567 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073705574 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 72968 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7297488098688 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7297488199590 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7613030979647 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8445290964595 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 8445291638839 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 884912126115 not in frontend and not explained in _meta exclusions
  WARN: Displayed barcode 3560070826186 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 5010026515919 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 5010026521149 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290011668570 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290019603634 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290114603034 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7290120871069 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7297488099821 has no BSIP2 trace in --run dir (ghost product)
  WARN: Displayed barcode 7613035758834 has no BSIP2 trace in --run dir (ghost product)

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [FAIL] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290120871069: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7297488099821: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5010026515919: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290114603034: no trace found in --run dir, cannot verify score vs trace
  FAIL: barcode=7290013433244: JSON grade=C but score=65 implies grade=B (policy=floor)
  FAIL: barcode=7290013433244: JSON score=65 vs trace score=63.0 (rounded trace=63, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290112498007: JSON score=62 vs trace score=62.7 (rounded trace=63, diff=1.000 > tolerance=0.05)
  WARN: barcode=7290019603634: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5010026521149: no trace found in --run dir, cannot verify score vs trace
  FAIL: barcode=7290013433091: JSON score=54 vs trace score=51.9 (rounded trace=52, diff=2.000 > tolerance=0.05)
  WARN: barcode=7290011668570: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=3560070826186: no trace found in --run dir, cannot verify score vs trace
  FAIL: barcode=7290013433107: JSON score=49 vs trace score=47.0 (rounded trace=47, diff=2.000 > tolerance=0.05)
  FAIL: barcode=6582751: JSON score=49 vs trace score=47.0 (rounded trace=47, diff=2.000 > tolerance=0.05)
  WARN: barcode=7613035758834: no trace found in --run dir, cannot verify score vs trace
  FAIL: barcode=7290011131371: JSON score=46 vs trace score=44.0 (rounded trace=44, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290011131388: JSON score=44 vs trace score=42.6 (rounded trace=43, diff=1.000 > tolerance=0.05)
  FAIL: barcode=7290011131050: JSON score=41 vs trace score=39.8 (rounded trace=40, diff=1.000 > tolerance=0.05)
  FAIL: barcode=7613037012095: JSON score=41 vs trace score=39.4 (rounded trace=39, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7613035635845: JSON score=41 vs trace score=39.4 (rounded trace=39, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290011131968: JSON score=40 vs trace score=37.9 (rounded trace=38, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290014471412: JSON score=40 vs trace score=38.0 (rounded trace=38, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290016883183: JSON score=38 vs trace score=36.0 (rounded trace=36, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290014471436: JSON score=36 vs trace score=34.4 (rounded trace=34, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290014471436: displayed grade=D is better than trace-derived grade=E (trace_score=34.4) — grade inflation
  FAIL: barcode=7290011131975: JSON score=33 vs trace score=31.7 (rounded trace=32, diff=1.000 > tolerance=0.05)
  FAIL: barcode=1343845: JSON score=33 vs trace score=31.1 (rounded trace=31, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290014471429: JSON score=32 vs trace score=30.2 (rounded trace=30, diff=2.000 > tolerance=0.05)
  FAIL: barcode=7290011131395: JSON score=26 vs trace score=24.4 (rounded trace=24, diff=2.000 > tolerance=0.05)

### [FAIL] G6 COPY-SAFETY
  FAIL: barcode=5018357006755 field=rowVerdict: banned phrase 'חלבון נמוך' found
  FAIL: barcode=5018357006755 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=6582751 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290011131388 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290014471412 field=rowVerdict: sodium causally framed: 'כי 400 מ"ג נתרן'
  FAIL: barcode=7613035622623 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290016883183 field=expansion.limitingFactors[1]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290014471436 field=rowVerdict: sodium causally framed: 'כי 400 מ"ג נתרן'
  FAIL: barcode=7290014471436 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=1343845 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290014471429 field=rowVerdict: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290014471429 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found
  FAIL: barcode=7290011131395 field=rowVerdict: sodium causally framed: 'כי 350 מ"ג נתרן'
  FAIL: barcode=7290011131395 field=expansion.limitingFactors[0]: banned phrase 'חלבון נמוך' found

### [SKIP] G7 PARITY
  SKIP: No baseline provided
