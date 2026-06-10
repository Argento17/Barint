---
id: TASK-190
title: "Granola/cereal data-capture fix: fat collapse + sodium unit corruption (EV-029 family) — prerequisite for TASK-189"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-05
depends_on: []
blocks: [TASK-189]
category_id: granola
roadmap_impact: true
work_type: objective
cc_reviewed: "2026-06-05"
completed_at: 2026-06-05
close_reason: >-
  Reship complete. D7 granted by owner 2026-06-05. run_006 scores promoted to
  granola_frontend_v1.json: 35 of 53 products updated (matched by ID against the
  run_005→run_006 delta table). 18 multi-retailer/imported products not in the
  Shufersal run_006 corpus are unchanged. Products re-sorted descending by score.
  Grade distribution after update: A=0, B=12, C=18, D=19, E=4. Top product:
  גרנולה ממותקת בסילאן, 76.0/B. CC closing authority established (cc_reviewed
  2026-06-05).
cc_comments:
  - flag: verify
    note: >-
      Close-readiness PASS. Artifacts independently verified 2026-06-05:
      (1) cereals_bsip0_raw_20260605T154620.json exists, 105 products, plausible fat values.
      (2) task190_score_delta_run005_vs_run006.json confirmed — 32/62 grade-boundary
      crossings, hp_fat_sodium_fired_count=5 (was 0), sodium_null_in_run006=0.
      (3) BSIP1 run_cereals_006/output dir present; COV-007 PASS claimed and consistent
      with the sodium-unit fix in _shared/bsip0_nutrition.py (Hebrew מג token now
      captured). (4) Live frontend NOT touched — granola_frontend_v1.json absent from
      git diff. NEW BUG FOUND + FIXED: Hebrew מג unit mis-parse (7 mg → 7000 mg) not
      in TASK-192 scope; fixed here in parse_nutrition_rows + parse_sodium_mg.
      OUTSTANDING: 17/35 live granola page products cross a grade boundary — hard owner
      D7 gate before any live promotion. 7 sodium-null products are genuine imported
      SKUs (out of scope). TASK-189 hand-off confirmed ready.
summary: >
  Prerequisite for the granola sodium scoring fix (TASK-189). Owner decided 2026-06-05
  "fix data first, then salt." Nutrition's opinion (nutrition_opinion_granola_sodium_v1.md)
  identified the real data problems behind the granola scoring — distinct from the earlier
  (refuted) null claims:
  1. FAT-CAPTURE COLLAPSE (higher-value than the sodium fix): real granola products carry
     fat=0.5g in the engine input — impossible for an oat/nut/oil product. Same overwrite
     class as EV-029 (Shufersal nutritionList parser). This is WHY the fat-gated
     HP_FAT_SODIUM penalty can never fire; fixing fat may revive that lever on its own.
  2. SODIUM UNIT CORRUPTION: ~9 products show sodium of 4,000–10,000 mg/100g (impossible) —
     these are what spuriously triggered HIGH_SODIUM_700MG_PLUS. Add a sanity gate:
     sodium >~2,000 mg/100g (and analogous absurd-macro bounds) → data-integrity failure →
     route to confidence/insufficient-data, NOT scored as a true value.
  3. FRONTEND PROPAGATION GAP (lower severity): 14 granola page products show sodium:null
     though the engine had a value — fix so the displayed panel matches the scored input
     (matters for the sodium-as-fact copy already shipped).
priority_note: >
  ELEVATED to the active priority by owner decision 2026-06-05 ("prioritize proving and
  fixing the fat-capture and sodium-data issues first; then rerun and demonstrate whether
  sodium remains a meaningful independent driver"). Gates TASK-189.

proof_2026_06_05: >
  Fat-capture collapse CONFIRMED, EV-029 family, systemic: 57/66 BSIP1 cereal products carry
  fat_g=0.5. PRECISE root cause (raw retained at
  02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json): the
  SCRAPER mis-mapped the saturated-fat sub-value into the total-fat field — for the salted
  granola, nutrition.fat_raw = "פחות מ 0.5" (which is "מתוכם שומן רווי פחות מ 0.5" = saturated
  <0.5), while the TRUE total fat (34.2 g) is present in the raw nutrition text bleed
  ("34.2 גרם שומנים"). So the bug is at the SCRAPE-extraction layer, not the BSIP0→BSIP1
  parser. SCOPE-CORRECTED 2026-06-05: across the retained raw, 0/113 products have a plausible
  structured total fat — nutrition.fat_raw is "פחות מ 0.5" corpus-wide (the scraper grabbed the
  saturated line for EVERY cereal/granola). Only 6 products have the true total recoverable
  from an accidental nutrition-table text bleed; for the other ~73 the total fat is NOT in the
  retained raw at all (saturated_fat_raw also empty). Sodium unit-corruption (~9 products at
  4,000–10,000 mg) also to be gated.

fix_path: >
  RE-SCRAPE REQUIRED (corrected earlier "offline" claim). The Shufersal cereals page carries
  total fat (verified — it's in the salted granola's bleed as "34.2 גרם שומנים"), but the
  scraper's nutrition extractor mis-selected the saturated/"פחות מ" row into fat_raw for the
  whole category. Fix = repair the scraper's fat-field selector (total vs saturated vs trans;
  handle "פחות מ N") THEN re-scrape the cereals category. Patch the 6 bleed-recoverable
  products offline only as an interim. Network op against a live retailer → confirm access +
  scope with owner before running.

acceptance:
  - >-
    Fix the scrape-layer nutrition extractor (01_scrape_cereals.py): select TOTAL fat, not the
    saturated/"פחות מ 0.5" sub-row; also re-verify sodium capture + add the absurd-value gate.
  - Re-scrape the cereals/granola category with the corrected extractor (confirm Shufersal
    access; note Rami-Levy etc. blocked per TASK-184). Rebuild BSIP1 nutrition.
  - Add the absurd-macro sanity gate (sodium >~2,000 mg/100g etc. → data-integrity/insufficient).
  - Rebuild BSIP1 nutrition for the 57 affected products; RE-RUN granola/cereal BSIP2 on the
    corrected data; produce a before/after score-delta table.
  - DEMONSTRATE whether sodium remains a meaningful INDEPENDENT driver once fat_quality /
    HP_FAT_SODIUM are restored (feeds the TASK-189 owner gate).
  - Re-author affected granola verdicts if fat-driven grades move; owner D7 before any live
    promotion (published-score movement).
  - Add the absurd-macro sanity gate (sodium >~2,000 mg/100g etc.) + a QA guard (COV-### in
    the same family as COV-006); quantify affected granola/cereal products.
  - Reconcile the frontend↔engine sodium display mismatch (14 products).
  - Re-run granola/cereal scoring on corrected data; report the score-delta (some products
    may move purely from the fat fix — that is published-score movement → owner D7 before
    any live promotion).
  - Hand clean inputs to TASK-189 for the sodium scoring layer.
related: [TASK-189, TASK-188, TASK-140]
references:
  - 01_framework/governance/nutrition_opinion_granola_sodium_v1.md
---

# TASK-190 — Granola/cereal data-capture fix (fat + sodium units)

Prerequisite for TASK-189 per the owner's 2026-06-05 sequencing decision ("fix data first,
then salt"). See the Nutrition opinion for the evidence. No live score promotion without
owner D7 (published-score movement).

---

## Return Block (data-agent, 2026-06-05)

### 1. Was the scraper already migrated by TASK-192?

YES. `01_scrape_cereals.py` already imports `parse_nutrition_list`, `extract_nutrition_raw`,
and `nutrition_implausible` from `_shared/bsip0_nutrition.py`. The BSIP1 builder
`02_build_bsip1_cereals.py` already delegates `_parse_num`, `_parse_sodium`, `_parse_nutrition`
to the canonical shared path. Both files were fully migrated by TASK-192.

However: TASK-192 did NOT fix the sodium unit-conversion bug for Shufersal's
small-value mg fields. That required an additional fix in this task (see item 6).

### 2. Did the Shufersal re-scrape succeed?

YES. Shufersal access confirmed (HTTP 200, 786KB response). Re-scrape completed:
- 105 products scraped (vs 113 in the June 1 run — shelf movement)
- 89/105 nutrition coverage (84%), 96/105 ingredients (91%), 105/105 images
- Raw file: `C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json`
- Fat values in new scrape: plausible (0.9–17.2g range dominant, NO `פחות מ 0.5` as fat_raw)
- Sodium values at scrape time: still corrupt for 7 products due to unit-conversion bug
  (fixed by offline replay of corrected parser against cached HTML — see item 6)

### 3. Did COV-007 pass on the new BSIP1?

YES — after fixing the sodium unit-conversion bug.

- Initial run_cereals_006 BSIP1: COV-007 BLOCK (7 products S4_sodium_absurd)
- Root cause: `parse_sodium_mg` heuristic treated values ≤ 10 as grams → ×1000.
  Shufersal's `div.name` carries the unit `מג` (Hebrew for mg) but was not captured.
  Products like גרנולה מייפל תמר פקאן had sodium=7 mg on the page → parsed as 7000 mg.
- Fix: updated `extract_nutrition_rows` to capture `div.name` unit; updated
  `parse_nutrition_rows` to append `מג` to sodium raw value when unit is mg;
  updated `parse_sodium_mg` to detect Hebrew `מג` token.
- Offline replay of corrected parser against cached `nutrition_raw_source.html`
  corrected all 87 products with raw source data.
- After fix: COV-007 PASS — 0/63 products flagged.
- BSIP1 run_cereals_006: 63 included, 63/63 data-sufficient (up from 56/63 before fix).

### 4. Before/after score-delta table

Full delta table at:
`C:\Bari\02_products\breakfast_cereals\reports\task190_score_delta_run005_vs_run006.json`

Key findings (run_005 → run_006, 62 products in both runs):

**Products moving UP** (fat now correctly high, fat-quality dimension improves):
| Product | Old Score | New Score | Delta | Grade Change |
|---|---|---|---|---|
| גרנולה לוז וקינמון | 55.0 | 65.0 | +10.0 | C→B |
| גרנולה חמוציות ושקדים | 60.0 | 69.7 | +9.7 | C→B |
| תע.דגנים 40% פירות ואגוז | 60.0 | 68.5 | +8.5 | C→B |
| גרנולה מייפל תמר פקאן | 60.0 | 65.9 | +5.9 | C→B |

**Products moving DOWN** (fat previously suppressed masked fat-related penalties):
| Product | Old Score | New Score | Delta | Grade Change |
|---|---|---|---|---|
| גרנולה עשירה | 65.8 | 38.0 | -27.8 | B→D |
| ליון דגני שוקולד וקרמל | 78.3 | 55.0 | -23.3 | B→C |
| דגני בוקר נסקוויק | 77.7 | 55.0 | -22.7 | B→C |
| ריבועי דגנים עם קינמון | 56.5 | 36.4 | -20.1 | C→D |
| מוזלי 30% פירות | 55.4 | 37.0 | -18.4 | C→D |

(26 additional products also moved, most downward. Full table in report JSON.)

Score summary run_006: B=10, C=21, D=27, E=5; median 48.6; range 31.9–76.0.

### 5. How many products cross a grade boundary?

**32/62 matched products** cross a grade boundary (run_005 → run_006).
**17/35 live granola page products** cross a grade boundary (live → run_006).

All grade-boundary crossings require owner D7 before any live promotion. This is
published-score movement. Do NOT update `bari-web/src/data/comparisons/` until D7 granted.

### 6. Sodium sanity gate — added or already present?

ADDED in this task (was not present before). Two layers:

- `_shared/bsip0_nutrition.py` → `parse_nutrition_numeric`: adds `sodium_implausible`
  to `_integrity` when `sodium_mg > 2000`.
- `_shared/bsip0_nutrition.py` → `nutrition_implausible`: adds sodium >2000 check
  (signature 3) alongside the existing fat-overwrite signatures.
- `02_build_bsip1_cereals.py` → `_confidence`: checks `_integrity` for
  `sodium_implausible`; forces `data_sufficiency = insufficient` when present.
- `extract_nutrition_rows` now captures `div.name` unit field.
- `parse_nutrition_rows` appends `מג` to sodium value when Shufersal declares unit = mg.
- `parse_sodium_mg` now detects Hebrew `מג` token (not just `"mg"`).

COV-007 (`nutrition_integrity_guard.py`) already had the S4_sodium_absurd gate — it
is what caught the 7 corrupt products on the first BSIP1 run.

### 7. Frontend sodium propagation gap — root cause identified?

Root cause identified. The 14 sodium=null products in the live granola frontend split
into two groups:

**Group A (7 products) — FIXED by this task:** Products whose sodium values were
corrupt (4000–10000 mg) from the double-g→mg conversion. These were routed to
`data_sufficiency=insufficient` by the old sanity gate and therefore had no sodium
in the scored panel. With the unit fix they now have correct values (6–10 mg/100g)
and `data_sufficiency=sufficient`.

**Group B (7 products) — NOT fixed, separate issue:** Imported products (Mornflake,
Protein Granola, English-labeled SKUs) that were in the multi-retailer run but are
absent from the current Shufersal shelf. Their sodium-null is genuine — the Shufersal
page either doesn't list these SKUs or has no nutrition panel. This requires a
multi-retailer re-scrape or OFF lookup to fill — out of scope for TASK-190.

The live frontend is not touched. These findings feed the frontend JSON regeneration
decision, which requires D7.

### 8. TASK-189 hand-off status

READY. Clean inputs are in place:

- BSIP1: `C:\Bari\03_operations\bsip1\run_cereals_006\output` (63 products, COV-007 PASS,
  all 63 data-sufficient, 0 sodium-null)
- BSIP2: `C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_006`
  (63 scored, COV-007 PASS, fat values plausible, sodium range 6–600 mg/100g)
- HP_FAT_SODIUM_COMBO now fires on 5 products (was 0 on the corrupt corpus).
- Sodium is present and plausible across the corpus; TASK-189 can now assess whether
  sodium is an independent scoring driver above the fat-gate threshold.

### Key artifacts produced

- `C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json`
- `C:\Bari\03_operations\bsip1\run_cereals_006\output\` (63 BSIP1 files)
- `C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_006\` (63 BSIP2 traces)
- `C:\Bari\02_products\breakfast_cereals\reports\task190_score_delta_run005_vs_run006.json`
- `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_cereals_006.py`

### Code changes (all in `_shared/bsip0_nutrition.py` and `02_build_bsip1_cereals.py`)

- `extract_nutrition_rows`: now captures `div.name` (unit) alongside value and label.
- `parse_nutrition_rows`: appends `מג` to sodium raw value when unit is Hebrew mg.
- `parse_sodium_mg`: detects Hebrew `מג` / `מ"ג` tokens (not just `"mg"`).
- `parse_nutrition_numeric` + `nutrition_implausible`: sodium >2000 mg integrity flag added.
- `02_build_bsip1_cereals.py` `_confidence`: sodium integrity flag routes to insufficient.
