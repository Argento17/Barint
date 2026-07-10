# Bari Page Generator — Gate Report

**Input:** `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json`
**Generated:** 2026-07-10T09:16:47Z  |  **Elapsed:** 0.1s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [WARN] G3 SCOPE | WARN |
| [PASS] G4 OFF | PASS |
| [WARN] G5 GRADE-INTEGRITY | WARN |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 117/117 non-null
  INFO: name: 117/117 non-null
  INFO: score: 117/117 non-null
  INFO: grade: 117/117 non-null
  INFO: insightLine: 117/117 non-null
  INFO: expansion: 117/117
  INFO: expansion.ingredients: 117/117
  INFO: expansion.nutrition.energyKcal: 117/117
  INFO: expansion.nutrition.protein: 117/117
  INFO: expansion.nutrition.sugar: 112/117
  INFO: expansion.nutrition.fat: 117/117
  INFO: expansion.nutrition.fiber: 73/117
  INFO: expansion.nutrition.sodium: 117/117
  INFO: expansion.confidenceLabel: 117/117
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 milk-depth coverage checks: SKIP (schema_version='', not v3)

### [WARN] G3 SCOPE
  INFO: Displayed products: 117
  WARN: Run directory not found: None

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [WARN] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor
  WARN: barcode=7290013453693: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013453068: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043149: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=80083764: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017962139: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290020030184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290122781359: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740113: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=540160: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740137: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740557: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043743: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=960860015432: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740472: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=311463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013453501: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740540: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740052: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740229: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740342: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740465: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013156921: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018371930: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018371923: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000061245: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5317194: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290011489625: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018371947: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119041053: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119041107: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119041152: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893845: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013156006: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740014: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017894317: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2986065: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290017898506: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=2986058: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118423904: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118422617: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106571945: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=313184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077614699: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453857: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019293804: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073453840: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410376037784: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290118426615: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816034: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106571921: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8410376075915: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4820180816590: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=80083665: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019870470: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4820180816576: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043798: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290013740694: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290123330488: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077633317: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=313160: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=311708: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8008698037171: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=74184: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4006529002170: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119041206: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119041350: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043095: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073162001: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290018893036: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=311128: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040803: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040858: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5410126006049: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5410126116168: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5410126726244: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5410126806250: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4823077614675: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290105364784: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502139017: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4820180816552: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502279010: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112961754: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502405204: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4017100198151: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=99804: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119043897: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073529019: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300489427: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=46214731552: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073529026: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=4017100364112: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8000500366073: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622210137234: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=5901414200411: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=46214930207: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300356767: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=61245: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7296073161981: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290106656727: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816232: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019870463: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502470028: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201401900: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040605: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040650: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622300489434: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290112340276: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290115206333: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290000075143: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622201809188: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290101111986: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=8710502064814: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290119040179: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290019816058: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7622210453327: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290109354996: no trace found in --run dir, cannot verify score vs trace
  WARN: barcode=7290109354972: no trace found in --run dir, cannot verify score vs trace
  INFO: All grade/score checks passed

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
