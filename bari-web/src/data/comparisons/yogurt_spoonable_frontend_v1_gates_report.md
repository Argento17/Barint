# Bari Page Generator — Gate Report

**Input:** `C:/bari_wt_yg/bari-web/src/data/comparisons/yogurt_spoonable_frontend_v1.json`
**Generated:** 2026-07-10T06:23:22Z  |  **Elapsed:** 0.2s

## Summary

| Gate | Status |
|------|--------|
| [PASS] G1 SCHEMA | PASS |
| [WARN] G2 COVERAGE | WARN |
| [PASS] G3 SCOPE | PASS |
| [PASS] G4 OFF | PASS |
| [PASS] G5 GRADE-INTEGRITY | PASS |
| [PASS] G6 COPY-SAFETY | PASS |
| [SKIP] G7 PARITY | SKIP |
| [PASS] G8 DATA-SANITY | PASS |

**Overall: PASS**

## Detail

### [PASS] G1 SCHEMA
  INFO: Document validates against schema

### [WARN] G2 COVERAGE
  INFO: imageUrl: 50/50 non-null
  INFO: name: 50/50 non-null
  INFO: score: 50/50 non-null
  INFO: grade: 50/50 non-null
  INFO: insightLine: 50/50 non-null
  INFO: expansion: 50/50
  INFO: expansion.ingredients: 50/50
  INFO: expansion.nutrition.energyKcal: 50/50
  INFO: expansion.nutrition.protein: 50/50
  INFO: expansion.nutrition.sugar: 50/50
  INFO: expansion.nutrition.fat: 50/50
  INFO: expansion.nutrition.fiber: 21/50
  INFO: expansion.nutrition.sodium: 50/50
  INFO: expansion.confidenceLabel: 50/50
  WARN: No corpus provided — imageUrl regression check skipped
  INFO: name: all products have Hebrew characters in name
  INFO: verdict coverage: every product has an authored insightLine or rowVerdict
  INFO: v3 consumerTakeaway: 0/50 authored (0 PENDING)
  INFO: v3 consumerExplanation.whyRated: 0/50 authored (0 PENDING, 50 not used by this page)
  INFO: v3 bariInterpretation.interpretation: 0/0 authored (0 PENDING)
  INFO: v3 bestUseCases: 0/50 authored (0 PENDING, 50 not used by this page)

### [PASS] G3 SCOPE
  INFO: Displayed products: 50
  INFO: Scored products (trace dirs): 94
  INFO: Declared exclusions in _meta: 44
  INFO:   missing barcode 408316: excluded — TASK-546 near-duplicate cull: name-reordered duplicate of kept product (identical ingredients/macros) (cluster danone_bio_3pct; kept representative 5839078). Scored but not displayed.
  INFO:   missing barcode 43944: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 45771: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 5416415: excluded — TASK-515 owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 57149: excluded — TASK-515 dedup-drop: byte-identical duplicate of canonical EAN-13 7290014758100 (KEPT).
  INFO:   missing barcode 6664990: excluded — TASK-546 near-duplicate cull: name-reordered duplicate (identical ingredients/macros) (cluster danone_bio_1_7pct; kept representative 4584528). Scored but not displayed.
  INFO:   missing barcode 7290014758117: excluded — TASK-515 dedup-drop (owner ruling): byte-identical duplicate of clean twin 57132 (KEPT); also carried confirmed Class-D diabetes-seal contamination -- dropping removes both the duplicate and the contamination in one action.
  INFO:   missing barcode 7290102390465: excluded — TASK-546 near-duplicate cull: Muller-labeled but byte-identical formula/macros to the unbranded Prof line (added on ingredient-match evidence; owner's own words 'completely similar just different package' directly describes this case) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290102390489: excluded — TASK-546 near-duplicate cull: flavor variant of same line (verified matching formula; not in owner's literal 3-item list, added on ingredient-match evidence) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290102391844: excluded — TASK-546 near-duplicate cull: flavor variant of same line (added on ingredient-match evidence) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290102393176: excluded — TASK-546 near-duplicate cull: flavor variant of same 3% fat line (E-1422/pectin formula); kept highest-score תות (cluster fruit_3pct_family; kept representative 7290102393169). Scored but not displayed.
  INFO:   missing barcode 7290102393947: excluded — TASK-546 near-duplicate cull: flavor variant of same 3% fat line (cluster fruit_3pct_family; kept representative 7290102393169). Scored but not displayed.
  INFO:   missing barcode 7290102399635: excluded — TASK-546 near-duplicate cull: flavor variant of same line (added on ingredient-match evidence) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290102399819: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster muller_protein; kept representative 7290102399802). Scored but not displayed.
  INFO:   missing barcode 7290107936309: excluded — TASK-546 near-duplicate cull: byte-identical ingredients/macros to kept product; same product under two listings (cluster greek_6_5pct; kept representative 7290115678222). Scored but not displayed.
  INFO:   missing barcode 7290110321031: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290110321680: excluded — TASK-546 near-duplicate cull: flavor variant of same Yoplait GO line (cluster yoplait_go; kept representative 7290110321697). Scored but not displayed.
  INFO:   missing barcode 7290110321703: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster yoplait_go; kept representative 7290110321697). Scored but not displayed.
  INFO:   missing barcode 7290110328627: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster yoplait_go_creamy; kept representative 7290110328764). Scored but not displayed.
  INFO:   missing barcode 7290110328788: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290110329952: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290110566975: excluded — TASK-546 near-duplicate cull: flavor variant of same line (verified matching formula; 3rd member found beyond owner's literal 2-item list) (cluster danone_pro_20g_0pct; kept representative 7290112330352). Scored but not displayed.
  INFO:   missing barcode 7290110578572: excluded — TASK-551 relocated to the drinkable-yogurt page: retailer category משקאות-יוגורט (Actimel drink). Re-scored under the drinkable config = identical grade. Scored here but displayed on /hashvaot/yogurt-drinks.
  INFO:   missing barcode 7290112330390: excluded — TASK-546 near-duplicate cull: flavor variant of same line (added on ingredient-match evidence) (cluster danone_pro_20g_0pct; kept representative 7290112330352). Scored but not displayed.
  INFO:   missing barcode 7290114311359: excluded — TASK-546 near-duplicate cull: flavor variant of same whipped-mousse line (E-1442/fish gelatin/tricalcium phosphate formula); kept highest-score תות (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290114312424: excluded — TASK-546 near-duplicate cull: flavor variant of same line (added on ingredient-match evidence) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290114312431: excluded — TASK-546 near-duplicate cull: flavor variant of same line (added on ingredient-match evidence) (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290114313070: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster mukzaf_whipped; kept representative 7290114310406). Scored but not displayed.
  INFO:   missing barcode 7290114314053: excluded — TASK-546 near-duplicate cull: flavor variant of same 3% fat line (verified matching formula/macros; not in owner's literal 4-item list, added on ingredient-match evidence) (cluster fruit_3pct_family; kept representative 7290102393169). Scored but not displayed.
  INFO:   missing barcode 7290114314060: excluded — TASK-546 near-duplicate cull: flavor variant of same 3% fat line (cluster fruit_3pct_family; kept representative 7290102393169). Scored but not displayed.
  INFO:   missing barcode 7290114314503: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster prof_whipped_family; kept representative 7290102390427). Scored but not displayed.
  INFO:   missing barcode 7290116932484: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116934402: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116935614: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116935621: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936123: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936215: excluded — TASK-515 owner-directed dump: sugars_g + fat_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936222: excluded — TASK-515 owner-directed dump: sugars_g unrecoverable across all 4 retailers (rescrape acc0c9ac).
  INFO:   missing barcode 7290116936581: excluded — TASK-515 owner-directed dump: field unrecoverable across all 4 retailers (rescrape acc0c9ac). Class A source-implausible single-ingredient milk declaration (10.0g/100g protein) -- missing_data_discard_rule.
  INFO:   missing barcode 7290119370177: excluded — TASK-546 near-duplicate cull: flavor variant of same Danone Pro 10g lactose-free/low-sugar line (cluster danone_pro_10g_lowsugar; kept representative 7290119370955). Scored but not displayed.
  INFO:   missing barcode 7290119372997: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster danone_pro_10g_lowsugar; kept representative 7290119370955). Scored but not displayed.
  INFO:   missing barcode 7290119377404: excluded — TASK-546 near-duplicate cull: flavor variant of same line (cluster danone_pro_25g; kept representative 7290119377411). Scored but not displayed.
  INFO:   missing barcode 7290119380916: excluded — TASK-551 relocated to the drinkable-yogurt page: retailer category משקאות-יוגורט (Actimel drink). Re-scored under the drinkable config = identical grade. Scored here but displayed on /hashvaot/yogurt-drinks.
  INFO:   missing barcode 7290119384242: excluded — TASK-546 near-duplicate cull: flavor variant of same line (verified matching formula; not in owner's literal 3-item list, added on ingredient-match evidence) (cluster danone_pro_10g_lowsugar; kept representative 7290119370955). Scored but not displayed.

### [PASS] G4 OFF
  INFO: No OFF markers detected in frontend JSON or displayed corpus records

### [PASS] G5 GRADE-INTEGRITY
  INFO: Boundary policy: floor

### [PASS] G6 COPY-SAFETY
  INFO: No copy-safety violations detected

### [SKIP] G7 PARITY
  SKIP: No baseline provided

### [PASS] G8 DATA-SANITY
  INFO: No data-sanity violations (impossible nutrition or nutrition-panel-as-ingredients)
