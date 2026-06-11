---
id: TASK-249
title: Yogurts v4 corpus remediation — parser disclaimer-strip (RT-2), macros_plausible gate (RT-1), Activia re-route (RT-3), additive E414 (RT-5), cultures detection (RT-12), copy templates (B-1/B-2/W-1), bio lens (B-4), full regen as run_yogurt_006
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  QA FAIL + red-team FAIL on rel/yogurts-v4 d6fcc2eb (run_yogurt_005). Root layer is the Shufersal ingredient parser counting website disclaimer text as ingredients (67/89 products, corrupts NOVA inference and the three 90/A grades) plus one protein=190 parse corruption that no gate blocked despite macros_plausible=false. Copy/filter blockers are template-level and ride the regen. Scores WILL move - rebuild outputs as run_yogurt_006, then QA + red-team re-audit. Yogurts v4 is DECOUPLED from the TASK-245 re-point (re-point ships master without it).
---

# TASK-249 — Yogurts v4 corpus remediation — full regen as run_yogurt_006

## Return Block

**Status:** RETURNED
**Date:** 2026-06-11
**Branch:** `task-249-corpus-remediation` (worktree at `C:\Bari\Bari-task249`)

### What Was Done

All Phase 1 (parser fixes) and Phase 2 (rebuild + TASK-250 rulings) work is complete.

#### Phase 1 — Parser fixes (BSIP1 run_yogurt_006)

| Fix | Status | Detail |
|-----|--------|--------|
| RT-2 Disclaimer strip | DONE | 63/88 products stripped; ingredient_text_quality="disclaimer_stripped" |
| RT-1 macros_plausible gate | DONE | barcode 7290116932620 protein=190 flagged; blocked at frontend |
| RT-3 Cereal misroute | DONE | barcode 7290112346797 excluded as cereal_misroute_excluded |
| RT-5 E414 detection | DONE | E414 added to ADDITIVE_TERMS; paren scan active |
| RT-12 Live cultures | DONE | FERMENTATION_TERMS updated; post-enrichment correction for bio/probiotic |
| RT-7 serving_size_g | DONE | Populated from weight_g for 50-250g single-serve containers |
| RT-10 Marketing prose | DONE | barcode 7290102395231 ingredient_text_quality=marketing_bleed; false honey sweetener neutralized |

#### Phase 2 — TASK-250 Methodology Rulings

| Ruling | Status | Detail |
|--------|--------|--------|
| Ruling 1: null sugar → confidence −10 | DONE | score_engine.py; 15 products affected; top-2 A-grade null-sugar products now conf=partial |
| Ruling 2: null satFat → confidence −5 | DONE | score_engine.py; RT-9 Greek targets (7290017065588, 7290014890589) now have real satFat values from disclaimer strip |
| Ruling 3: grade-before-round fix | DONE (gate) | build_yogurts_frontend_v006.py; 7290114313070=35/E, 7290102399819=50/D. OWNER SIGN-OFF REQUIRED BEFORE GO-LIVE |
| Ruling 4: sweetener detection gap | DONE | RT-2 resolved false detections for 2/3 products; Bio Natural (7290102395231) resolved by marketing_bleed detection |
| Ruling 5: ceiling compression disclosure | ROUTES TO CONTENT AGENT | No score change; category caveat copy update needed |

#### Copy Template Fixes

- "NOVA 4" removed from insightLine and limitingFactors — replaced with "עיבוד תעשייתי גבוה"
- Terminal "ציון X" removed from insightLine (score chip owns the grade)
- "מדד זה לא נכלל בניתוח" replaced with "ערך הסוכר לא היה זמין במקור הנתונים." / "ערך שומן הרווי לא היה זמין במקור הנתונים."
- Marketing-prose ingredients (barcode 7290102395231) hidden from frontend (ingr_text=None when marketing_bleed)

#### Shelf Filter / Frontend

- "bio" added to YogurtsShelfFilterId in yogurts-shelf-filters.ts with label "ביו/פרוביוטי"
- Cluster assertion added to builder: every _cluster value must be in VALID_CLUSTER_IDS

### Build Results

- BSIP1 run_yogurt_006: 88 included, 8 excluded (7 no_usable_nutrition, 1 cereal_misroute), 1 macros_plausible=False
- BSIP2 run_yogurt_006: 88 products, 0 errors
- Frontend: 88 products, 1 blocked (macros_plausible=False), grade distribution A:14 B:30 C:20 D:23 E:1
- tsc: PASS
- next build: PASS
- Config hash: cb575d2af1fe1b7f

### Key Score Movements (run_005 → run_006)

Grade changes (grade letter changed):
- 7290116932620: 89.9/A → BLOCKED (macros_plausible=False; protein=190 corruption)
- Multiple C→B promotions: disclaimer strip exposed clean NOVA2 ingredients
- Multiple B→A promotions: same reason
- 7290114313070: 35/D → 35/E (Ruling 3 grade-before-round fix)
- 7290102399819: 50/C → 50/D (Ruling 3 grade-before-round fix)
- 7290112336712: 90.4/S → 89.9/A (disclaimer strip removed false fermentation keywords; TRIM cap holds)

### Pre-Go-Live Gate

1. **TASK-250 Ruling 3 owner sign-off required before go-live** — two products change published grade (35/D→35/E and 50/C→50/D). Tripwire 2 applies.
2. **Ruling 5 category caveat copy** — Content Agent must update the yogurts "הערת קטגוריה" to include ceiling compression disclosure before launch.
3. **QA Agent baseline freeze** required on run_yogurt_006 artifacts before PR merge.

### Artifacts

All in worktree `C:\Bari\Bari-task249` (branch `task-249-corpus-remediation`):

- `03_operations/bsip0/scrape/shufersal_yogurt/02_build_bsip1_yogurt_006.py` — BSIP1 builder with all RT fixes
- `03_operations/bsip0/scrape/shufersal_yogurt/test_bsip1_yogurt_006_fixes.py` — 25 regression tests
- `03_operations/bsip1/core/ingredient_enricher.py` — E414 + Activia FERMENTATION_TERMS additions
- `03_operations/bsip2/proto_v0/src/score_engine.py` — Rulings 1+2 confidence reductions
- `03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py` — BSIP2 batch runner
- `02_products/yogurt_system/build_yogurts_frontend_v006.py` — Frontend builder with all fixes
- `02_products/yogurt_system/yogurts_frontend_v4.json` — Staging output (run_006 content)
- `02_products/yogurt_system/reports/run_yogurt_006_run_record.json` — Run record
- `bari-web/src/data/comparisons/yogurts_frontend_v4.json` — Web output (run_006 content)
- `bari-web/src/lib/comparisons/yogurts-shelf-filters.ts` — "bio" filter added

Run data in main repo (untracked, shared):
- `C:\Bari\03_operations\bsip1\run_yogurt_006\output\` — 88 BSIP1 records
- `C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006\` — 88 BSIP2 traces
- `C:\Bari\02_products\yogurt_system\reports\run_yogurt_006_run_summary.json` — Run summary
