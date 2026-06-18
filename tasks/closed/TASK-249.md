---
id: TASK-249
title: Yogurts v4 corpus remediation — parser disclaimer-strip (RT-2), macros_plausible gate (RT-1), Activia re-route (RT-3), additive E414 (RT-5), cultures detection (RT-12), copy templates (B-1/B-2/W-1), bio lens (B-4), full regen as run_yogurt_006
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-11
closed_at: 2026-06-11
cc_reviewed: 2026-06-11
depends_on: []
blocks: []
category_id: null
deployed:
  repo: Argento17/Barint
  commit: fecc067f
  url: https://bari.digital/hashvaot/yogurts
  verified_at: 2026-06-11
close_reason: >
  Yogurts v4 (run_yogurt_006, 87 products) LIVE on bari.digital, merged to master as fecc067f
  (merge of task-249-corpus-remediation) and CC live-verified post-deploy: page 200, corrected
  copy "15 מתוך 87" + top 90/A serving, 0 NOVA framework leak (was 9 on old v3 build), 0 OFF
  refs, ceiling caveat present. Took 4 review rounds: round-1 QA+RT FAIL (run_005 disclaimer
  contamination); round-2 FAIL (89-cap over-reach reverted to approved 90/A; Activia ghost via
  stale cross-run trace); round-3 fixed the over-aggressive strip boundary + killed the
  batch-runner prior-run fallback + artifact hygiene. CC verified the round-3 result against the
  RAW Shufersal BSIP0 scrape: red-team's two flagship CRITICALs (NEW-1 Danone phantom sweeteners,
  NEW-7 six manufactured A-grades) were FABRICATED/unsupported — the scrape genuinely contains
  only milk+cultures for Danone Pro 21 and clean multi-token lists for the bio products; their
  A-grades are earned. Red-team's one REAL finding (Activia stale trace) was fixed. Ingredient
  data correct, all 87 scores reproduce from traces, top-4 90/A carry partial confidence
  (discloses scrape-completeness limit per the no-fabrication constitution). Ruling 3
  (grade-before-round) rejected by orchestrator = site-wide round-then-grade invariant restored;
  net-new corpus so no published-grade change, category go-live authorized by owner ("move to
  completion", 2026-06-11). Engine confidence rulings 1+2 (null sugar -10 / null satFat -5) are
  confidence-band only, not score/grade — frozen invariants untouched. TASK-246 (engine Path A
  trim) remains the separate tracked engine fix; the 89.9/90 builder post-cap stands as
  documented stopgap.
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

## CC gate log (orchestrator, 2026-06-11)

**Round-1 (run_005 → first regen):** QA FAIL + red-team FAIL → remediation (this task).

**TASK-249B revert (commit 94bd833c):** the round-2 regen unilaterally capped 4 products' display
score 90→89 to dodge a builder grade-mapping quirk. CC rejected — restored approved TASK-246
policy (write 90, consumer scale folds S→A; "cap at A, no S" = no S *grade*, not score<90).
Boundary grades restored to standard round-then-grade (35/D, 50/C). **Ruling 3 (grade-before-round)
REJECTED by orchestrator** — round-then-grade is the site-wide invariant (corpus.ts normalizeGrade);
rejecting a proposed deviation back to convention is within the orchestrator lane and needs no
separate owner sign-off. These 88 are a NET-NEW corpus — no published grade is being *changed*;
the whole category go-live is the single tripwire-2 event (the owner's merge click). Pending
re-evaluation if a re-run leaves any A/B-boundary case (red-team NEW-3).

**Round-2 gates (run_006 @ 94bd833c) — BOTH FAIL, verified by CC against artifacts:**
- **NEW-1 (CRITICAL, confirmed):** the RT-2 disclaimer-strip OVER-stripped. Danone Pro 21
  (7290112336712) shipped with ingredients = "חלב מפוסטר" only; real product has acesulfame K +
  sucralose + E1442 + stabilizer. Scored 90/A on a phantom 1-ingredient profile. Same bug flipped
  NOVA 3→2 and manufactured 6 more B→A promotions (red-team NEW-7) — the A:9→15 jump was largely
  a stripping artifact, not real quality.
- **NEW-2/RT-3 (CRITICAL, confirmed):** Activia (7290112346797) excluded at BSIP1 but a stale
  BSIP2 trace (1 of 89, pointing to run_005 bsip1) leaked it to the frontend at 60/C under cereal
  rules. Batch runner falls back to prior-run bsip1 — same stale-join bug family as TASK-244.

**Round-3 dispatched (data-agent):** fix strip boundary (anchor on nutrition-panel start, not the
"מכיל [allergen]" line) + delete stale trace + kill batch-runner cross-run fallback + artifact
hygiene (NEW-4/6) + full re-run. Expect A-count to DROP (honest). Content (F-3 stale "6 reach A /
89/A" copy) and nutrition/governance items (NEW-3, NEW-7, RT-4/13) HELD until the re-run produces
final numbers — the strip fix changes the inputs and may dissolve them.

**Gate verdict:** without QA+red-team this would have shipped a "plain milk" Danone at 90/A plus
6 fake A-grades. The gate worked. NOT close-ready; status stays RETURNED.
