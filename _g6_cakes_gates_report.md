# Bari Page Generator — Gate Report

**Input:** `C:/Bari/_g6_cakes.json`
**Generated:** 2026-06-25T06:06:18Z  |  **Elapsed:** 0.2s

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
  FAIL: #.products[0].expansion: missing required field 'comparisonContext'
  FAIL: #.products[0].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[0].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[0].bariInterpretation: expected type ['array', 'null'], got str
  FAIL: #.products[0]: additional property 'consumerExplanation' not allowed
  FAIL: #.products[0]: additional property 'brand' not allowed
  FAIL: #.products[1].expansion: missing required field 'comparisonContext'
  FAIL: #.products[1].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[1].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[1].bariInterpretation: expected type ['array', 'null'], got str
  FAIL: #.products[1]: additional property 'consumerExplanation' not allowed
  FAIL: #.products[1]: additional property 'brand' not allowed
  FAIL: #.products[2].expansion: missing required field 'comparisonContext'
  FAIL: #.products[2].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: #.products[2].expansion.nutrition: additional property 'carbs' not allowed
  FAIL: #.products[2].bariInterpretation: expected type ['array', 'null'], got str
  FAIL: #.products[2]: additional property 'consumerExplanation' not allowed
  FAIL: #.products[2]: additional property 'brand' not allowed
  FAIL: #.products[3].expansion: missing required field 'comparisonContext'
  FAIL: #.products[3].expansion.nutrition: additional property 'satFat' not allowed
  FAIL: ... and 370 more errors

### [WARN] G2 COVERAGE
  INFO: imageUrl: 65/65 non-null
  INFO: name: 65/65 non-null
  INFO: score: 65/65 non-null
  INFO: grade: 65/65 non-null
  INFO: insightLine: 65/65 non-null
  INFO: expansion: 65/65
  INFO: expansion.ingredients: 65/65
  INFO: expansion.nutrition.energyKcal: 65/65
  INFO: expansion.nutrition.protein: 65/65
  INFO: expansion.nutrition.sugar: 64/65
  INFO: expansion.nutrition.fat: 65/65
  INFO: expansion.nutrition.fiber: 11/65
  INFO: expansion.nutrition.sodium: 65/65
  INFO: expansion.confidenceLabel: 65/65
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 65
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290119030095: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073346340: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5718021: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5431920: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290006983787: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119045013: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016162264: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5431913: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472261: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9399288: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472254: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472186: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1361207: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893661: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4504670: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119039746: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5718038: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472193: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119042302: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073346333: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893487: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106578821: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4504687: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4504649: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4504656: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073431893: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073132936: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4170103: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290006775023: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105692498: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073140184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9397642: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290111534010: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073431909: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472223: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6983794: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073431879: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073132950: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4170097: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290123330884: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6983787: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290016416961: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073431817: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073132943: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073431916: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472841: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=6983770: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290123331034: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073473664: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073473688: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=1361177: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290006775337: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013927996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290006775085: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013683595: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472117: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=9397697: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472087: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290012244032: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2472148: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015726528: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290012244056: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290015726535: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290123330280: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290123330334: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)

### [SKIP] G9 INVERSION-INVARIANT
  SKIP: No --run dir provided or directory not found — inversion check skipped
