---
id: TASK-474
title: Red-team report backfill for the 8 uncovered live categories (F2 launch-hardening)
owner: adversarial-qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-03
depends_on: []
blocks: []
category_id: null
summary: >
  P1 item 9a / report finding F2: 10-of-17 (canonically 8) live comparison categories have no red-team report on disk. Backfill an adversarial red-team report per category, highest-traffic first. Uncovered: bread, cakes, cheese, chocolate-bars, chocolate-tablets, crackers, milk, protein-bars. Batched one category per lane to avoid timeout. Internal reports (non-consumer); CRITICAL findings escalate.
---

# TASK-474 — Red-team report backfill for the 8 uncovered live categories (F2 launch-hardening)

## Batch 1 = BREAD — DELIVERED (report `02_products/bread/reports/red_team_bread_page_v1.md`, first-ever). Verdict: NO-GO. Top findings orchestrator-verified.

**Verified by orchestrator (against artifacts):**
- **Score drift (G5):** frontend bread_v3+v4 serve #1 product `7290016245325` at **94.8/S**, matching `run_bread_conform_001`; newer `run_bread_conform_002` (2026-07-01) computes **94.0/S**. Confirmed. Grade unchanged (S), 0.8pt = below ≤2pt noise floor. Frontend serves the older run.
- **Ingredient handoff loss (CRITICAL):** confirmed 6/6 sampled — bread BSIP1 `ingredient_order` populated (e.g. 1902325 = 12 items, 537-char text) but `ingredients_list=[]`; BSIP2 reads `ingredients_list` → scored `ingredient_count=0` (NOVA/structural/confidence degraded). Same root as crackers F3. **Scope not bread-only** (ingredient_count=0 appears across categories, but some legit-empty e.g. juices) → routed to **TASK-475 diagnosis** (scope + measured score impact; TRIPWIRE-1, no score changed).
- **HIGH-1 copy (em-dash + antithesis in all 23 bread lines):** the LIVE (pre-#51) copy — **likely already fixed by pending PR #51** (bread overhaul swept antithesis/em-dash). Confirm on #51 merge.
- **G3 (2 insufficient_data products dropped, no _meta disclosure):** likely correct per missing-data-discard rule, undocumented → data-agent follow-up.
- **Clean (verified):** OFF ban 0, no jargon, rank sanity, superlatives hold, null-honesty.

**Program status:** batch 1 (bread) done → TASK-475/476. Batch 2 (cheese) done — see below.

## Batch 2 = CHEESE (cheese_spreads) — DELIVERED (`02_products/cheese_spreads/reports/red_team_cheese_page_v1.md`). Verdict: NO-GO. Orchestrator VERIFIED + RE-CHARACTERIZED (red-team's headline is largely a FALSE ALARM):
- **Red-team claim:** score propagation broken 30/47, 2 "grade inflations" (3523230065467 B-vs-C, 7290019635581 D-vs-E), no committed run reproduces live v5 >32%.
- **Orchestrator verification (against origin/master LIVE v5 — note: LOCAL tree is DIVERGED, has v4; live loader reads v5, confirmed on origin/master + #51 branch):** LIVE v5 scores match NO committed run, BUT delta-vs-run_004 = **28/47 within 0.5pt, remainder a POSITIVE-only subset uplift up to +5.3** (mean +0.94, only 1 product −0.5). That distribution = the **cheese de-anchor (BARI_REDLABEL_V1, PR #34 owner-approved)** removing the binary red-label cap from affected products — NOT drift. The 2 "inflations" (C→B, E→D) are the red-label penalty being lifted as designed. **→ scores are LEGITIMATE, not broken.**
- **REAL finding (re-characterized):** a **traceability gap** — the owner-approved de-anchor was applied post-trace (frontend/transform) and never re-emitted as a committed BSIP2 run, so `run_gates` can't mechanically reproduce live cheese scores, and the prior go-live claim ("47/47 trace-exact PASS", commit e953c8d6) does not hold as stated. This is the F1/TASK-409 traceability class, not a scoring bug.
- **Secondary REAL (minor):** 12 scored barcodes absent from displayed 47 with only 6 documented exclusions (G3, needs _meta disclosure); stale _meta provenance date (June 26); shell copy (prologue/caveat, NOT row-copy overhaul scope) has em-dash + "X not Y" phrasing violations.
- **FIX class:** re-emit the de-anchored cheese scores as a committed trace run (hygiene, ZERO score change) + disclose exclusions + refresh provenance + shell-copy phrasing pass. NOT a rescore (scores are correct). Queue AFTER the bread rescore (avoid parallel score threads). Confirm-de-anchor-vs-drift diagnosis recommended before the trace re-emit to be 100% (pattern is strong but not each-product-proven).

**Pattern flag:** 2 red-teams (bread, cheese) → 2 score-integrity findings, both rooted in traceability/local↔origin gaps (F1/F3/TASK-409). Evidence the traceability reconciliation is a genuine launch risk. Remaining backfill: protein-bars (defer till post-rescore), cakes, chocolate-bars, chocolate-tablets, milk.

## Batch 3 = CAKES — DELIVERED (`02_products/cakes/reports/red_team_cakes_page_v1.md`, 421 lines, first-ever; first attempt died on API disconnect, re-run clean w/ incremental-write). Verdict: GO-WITH-FINDINGS (1 CRIT / 2 HIGH / 3 MED). Read @ origin/master de8c7801.
- **CRIT F-C1 (orchestrator-VERIFIED against origin/master):** live cakes JSON caveat body line 60 = `כל 63 המוצרים` but corpus = **62** (grades C:1/D:1/E:60 confirmed); 3 filter chips over-promise (least_bad "ציון D" says 2, only 1 D exists; has_phvo 20→~18; no_phvo 45→~44). Baked page_copy strings, render verbatim (component doesn't recompute). Consumer-facing accuracy bug, NOT a wrong score. **→ FIX TASK-480 dispatched** (Content lane, worktree fix/task480-cakes-accuracy, two-gate → owner PR).
- **HIGH F-V1 (traceability, NOT wrong-score):** no committed BSIP2 trace reproduces live cakes scores in one shot — all 3 run dirs predate TASK-439 reflow + 2026-07-02 de-anchor; every sampled delta explained by named two-gate-signed commits, but reproduction needs replaying 2 chained diffs. **SAME class as bread/cheese F1/TASK-409** → joins the traceability-reconciliation program (re-emit committed trace run, ZERO score change). 3rd red-team in a row with this finding.
- **HIGH F-C2:** 2 antithesis "X not Y" (caveat + product 1361207 rowVerdict) → folded into TASK-480. **MED:** F-V2 84 excluded share circular reason "not_in_live_curation" (G3 config hygiene); F-C3 confidence tooltip claims "all scraped" while 82% null fiber (confidence-honesty, check if shared tooltip before fixing); F-C4 8 em-dashes → TASK-480.
- **CLEAN (verified):** ingredient-handoff 5/5 (cakes NOT in REAL_LOSS-57, confirmed), OFF ban 0, rank/dedup/order integrity, **all 6 superlative claims rank-checked TRUE vs full 62-corpus** (700mg peak, highest sugar, muffin subgroups).

**Program status:** batch 3 (cakes) done → TASK-480 fix SHIPPED PR #60. Remaining: chocolate-tablets, milk (protein-bars post-rescore).

## Batch 4 = CHOCOLATE-BARS — DELIVERED (`02_products/chocolate/reports/red_team_chocolate_bars_page_v1.md`, sha 58328a8a). Verdict GO-WITH-FINDINGS (0 CRIT / 2 HIGH / 4 MED). Read @ origin/master. Route /hashvaot/chocolate-bars → chocolate_bars_frontend_v1.json (23 displayed of 29 scored bars; tablets separate).
- **F-C2 HIGH (orchestrator-VERIFIED):** banned "X not Y" antithesis + em-dash in the HERO TITLE — `chocolate-bars-comparison-page-data.ts:43` = "חטיפי השוקולד האלה הם חטיפי ממתק, לא חטיפי ביניים — וכולם יודעים את זה" + SEO meta (:68 "מידע, לא המלצה") + prologue em-dashes. Lives in the HARDCODED page-data.ts (hero/prologue/methodology/SEO), which the PR#51/#53 JSON overhaul + phrasing sweep NEVER touched. **→ SYSTEMIC (see below).**
- **F-C1 HIGH (orchestrator-VERIFIED):** the "אגוזים / בוטנים" shelf filter (`chocolate-bars-shelf-filters.ts:44-45`) matches `product.name.includes(kw)` for kw in [בוטן,אגוז,שקד,פיסטוק,קשיו] — NAME-ONLY, never ingredients. Silently excludes Snickers (#1, peanut-based, name has no nut word) + others whose nuts are in ingredients/driver. Code comment admits "conservative, name-only." Functional under-selection. → frontend/data fix (broaden to ingredient presence, or relabel honestly).
- **F-V1 HIGH (traceability, NOT wrong-score):** only committed trace (2026-06-24) scored all sampled under wrong category snack_bar_granola (pre-fix); TASK-455 f026f2dd (2026-07-02) reclassified+rescored, live = trace +0.9..+4.6, matches that commit's own "23/23 up, 0 flips." Cleaner than cakes (one named commit, not two). **4th category with the pattern.**
- **MED:** F-V2 count-methodology divergence; F-V3 6/29 excluded with bucket label only (G3); F-V4 no machine-checkable off_used flag. **CLEAN:** ingredient-handoff 5/5, OFF 0, rank/dedup, 8/8 superlatives TRUE, confidence honest, filter-count architecture live-computed (immune to cakes stale-count bug).

## ⚠️ SYSTEMIC FINDING (from F-C2) — page-narrative copy NEVER phrasing-swept
The copy overhaul (PR #51/#53) + phrasing sweep covered the frontend JSON (insightLine/rowVerdict/expansion). It did NOT cover the **6 bespoke `lib/comparisons/*-comparison-page-data.ts`** files that hold hero/prologue/methodology/SEO copy. Orchestrator-measured on origin/master (python, reliable): **23 antithesis + 84 em-dashes total** — bread 3/9, chocolate-bars 2/9, chocolate-tablets 2/9, hummus 3/20, protein-bars 10/23, snacks 3/14. NOTE some `לא` are intentional owner-voice rhetorical ("we don't tell you what to eat, we do…") → needs EDITORIAL judgment + two-gate, NOT a blind sweep. Recommend: ONE gated page-narrative phrasing pass across the 6 files (parallels the "one traceability pass" logic). SURFACED TO OWNER. **Traceability pattern now 4/4 (bread/cheese/cakes/chocolate-bars).**

## Batch 5 = CHOCOLATE-TABLETS — DELIVERED (`02_products/chocolate/reports/red_team_chocolate_tablets_page_v1.md`, sha f6d44eaf). Verdict GO-WITH-FINDINGS (1 CRIT / 3 HIGH / 3 MED). Read @ origin/master e615244a.
- **F-V3 CRITICAL (orchestrator-VERIFIED, real) → TASK-481:** 3 grade-C tablets (bc 3046920023429/368/443, score 50, distinct private-label names) excluded from the displayed 35 with NO documented reason (config exclusions=[], dedup per-barcode, subpool=all-tablets). Silent omission of legit products = completeness-promise breach. + stale _meta 33 vs 35. Full verified detail in TASK-481.
- **F-C1 HIGH:** shelf filters C/D/E only, but #1/#2 are B-grade co-leaders (65.8/65.1) → unreachable via filter. → TASK-481.
- **F-V1 HIGH traceability:** 5th category with the pattern (live scores from TASK-455 reclass, no committed run reproduces; explained by that one commit). **Pattern now 5/5.**
- **F-C2 HIGH:** 15 antithesis (12 JSON + 3 page-data.ts) + em-dashes → feeds systemic phrasing finding (NOTE: 12 in the overhauled JSON needs a spot-check — some `לא` may be owner-voice not violations; editorial call). **CLEAN:** ingredient-handoff 5/5, OFF 0, 6/6 superlatives TRUE, confidence honest, NO name-only filter bug (tablets filters grade-only).
- Display itself is HEALTHY (B:2/C:6/D:10/E:17 — real range, dark-choc leads correctly).

## Batch 6 = MILK (gold standard) — DELIVERED (`02_products/milk_and_alternatives/reports/red_team_milk_page_v1.md`, sha 6154842e). Verdict GO-WITH-FINDINGS (2 CRIT / 3 HIGH / 3 MED). Read @ origin/master. Both CRITICALs orchestrator-VERIFIED → **TASK-482**.
- **RT-1 CRIT:** 18/18 milk products labeled "נתונים מלאים"/"all scraped" while fat/satFat/carbs/fiber NULL 18/18 → false completeness. **RT-2 CRIT:** blog /blog/milk-analysis renders LEGACY `milkProducts` (milk-comparison.json, 48.5/**D**) vs live /hashvaot/milk-comparison corpus (51.7/**C**) — same barcode, grade-level contradiction, live now. (RT-3 almonds-for-oat = dead code, not rendered; RT-4 partial-data superlative; RT-5 antithesis in milk JSON → phrasing sweep.) Track V CLEAN (8/8 trace-exact, OFF 0, monotonic). Full detail + fix plan in TASK-482.

## PROGRAM STATUS: BACKFILL COMPLETE (6/6 live non-deferred categories)
Bread · cheese · cakes · chocolate-bars · chocolate-tablets · milk all red-teamed (first-ever reports on disk). protein-bars = the only remaining, DEFERRED to post-rescore (TASK-477). **No wrong published scores found anywhere.** Three cross-cutting launch-hardening outputs, all surfaced to owner for a batched decision:
- **(A) Traceability pattern 5/6** (bread/cheese/cakes/choc-bars/choc-tablets; milk is hand-curated gold-standard, expected): live scores correct but no single committed run reproduces them (de-anchor/reflow applied post-trace). → ONE reconciliation program (re-emit committed trace runs, ZERO score change).
- **(B) Systemic page-narrative phrasing gap:** 6 bespoke `*-comparison-page-data.ts` (+ milk JSON) hold hero/prologue/SEO copy never swept by the overhaul — 23 antithesis + 84 em-dash. Some `לא` = intentional owner-voice → needs EDITORIAL two-gate, not blind sweep. → ONE gated phrasing pass.
- **(C) Per-page defects registered:** TASK-480 cakes counts (SHIPPED #60), TASK-481 chocolate-tablets curation gap (3 grade-C hidden + stale _meta + no B chip; BLOCKED on sweep decision), TASK-482 milk 2× CRIT (BLOCKED on owner steer), chocolate-bars nuts-filter under-selection (name-only) + cheese traceability re-emit (batch 2).
