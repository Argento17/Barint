---
id: TASK-143
title: "Yogurts: re-run on calibrated engine + reconcile + retire DEC-005 (replace live manual shelf)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "Live swap shipped and verified; per the lifecycle rule only the Central Controller records CLOSED. I have not committed (you didn't ask) \u2014 say the word and I'll commit this on a branch."
returned_at: 2026-06-02
depends_on: [TASK-139, TASK-142A]
blocks: []
category_id: yogurts
returned_reason: "TASK-142A parser fix landed; blocker CLEARED. Clean re-run executed: re-scrape (corrupt 2026-06-01 raw replaced) -> BSIP1 run_yogurt_004 -> BSIP2 run_yogurt_004 (engine 0.4.0 UNMODIFIED). COV-006 0.0% implausible; fat=0.5 collapsed 47/97->1. EV-029 impact MILD (5/84 grade changes, median score delta 0.0) because yogurt fat is genuinely low. Reconciled vs run_003 (machine) + live DEC-005 manual shelf: confirmed downward correction (live A-heavy 5 A's vs machine B-capped, max 78.7; A-ceiling 139A does NOT restore A). DATA CYCLE DONE + CLEAN. Live swap HELD on two human gates: Product Owner go-live (retire DEC-005, accept A->B) + Content/Design re-author. No live frontend touched. See run_004 return block."
blocker: "CLEARED 2026-06-02 — TASK-142A parser fix landed; run_yogurt_004 is the clean re-run."
summary: >
  Carries forward the substance of CLOSED TASK-135. Per Product Owner decision (2026-06-01) yogurts is a FULL
  REPLACE via the calibrated engine: re-run the real Shufersal BSIP0->BSIP2 cycle on the post-TASK-139 engine,
  reconcile against the live manual shelf (document every grade delta), then retire DEC-005 and replace the
  live yogurt frontend dataset. Product Owner sign-off required for the live swap (this overwrites a live shelf).
---

# TASK-143 — Yogurts re-run + DEC-005 retirement

Supersedes the deferred substance of TASK-135 (CLOSED "not necessary for now"). Shufersal source already
validated (run_yogurt_003). **BLOCKED until TASK-139** (calibration) lands.

## Steps
1. Re-run full BSIP0->BSIP2 on the **calibrated** engine (enricher culture-vocab + router fix + A-ceiling ruling applied).
2. **Reconcile** vs the live DEC-005 manual shelf — document every score/grade delta. Expect downward correction (machine reads real sugar/starch/stabilizers); A-ceiling ruling (139A) may restore A for plain live-culture.
3. **QA**: hard-fail-free, BSIP2->BSIP0 traceability, freeze new baseline.
4. **Content/Design**: re-author insight lines/prologue to the new shelf; 15–20s comprehension test.
5. **Product Owner go-live**: confirm retiring DEC-005 + accepting the corrected (less flattering, more truthful) shelf.
6. **Data**: replace live `yogurts_frontend_v1.json` (root + bari-web sync); retire DEC-005.

## Exit / DoD
DEC-005 retired; live yogurt page reflects the calibrated machine shelf; every delta documented + justified;
QA baseline frozen + green; Product Owner go-live recorded. Then propose RETURNED.

---

## Return block — proposed RETURNED (data-agent, 2026-06-02) — run_yogurt_004 (clean, EV-029-corrected)

**Blocker CLEARED.** TASK-142A (EV-029 parser fix) is CLOSED and the yogurt scraper imports the shared fixed
parser. Executed the clean data cycle, **engine proto_v0 / 0.4.0 UNMODIFIED** (no score tuning, no router change).

**Run:** `run_yogurt_004` · supersedes run_yogurt_003 (AFFECTED by EV-029).

**Deliverables:**
- Re-scrape: `02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260602T064551.json` (corrupt 2026-06-01 raw **replaced/deleted**; `nutrition_raw_source` persisted per TASK-151 → future label-map fixes replay OFFLINE).
- BSIP1: `03_operations/bsip1/run_yogurt_004/output/` (86 records) via `02_build_bsip1_yogurt_004.py`.
- BSIP2: `02_products/yogurt_system/bsip2_outputs/run_yogurt_004/` (86 traces) via `proto_v0/src/batch_run_yogurt_004.py`.
- Reports: `reports/run_yogurt_004_run_summary.json`, `run_yogurt_004_qa_gate.json`, `reconciliation_143_run_yogurt_004_findings.md`.

**Data integrity validated:** fat=0.5 collapsed **47/97 → 1** (the 1 is a genuine 0% product). QA: COV-006
**0.0% implausible**, COV-001 95.3%, COV-002/003/005 100%. 0 pipeline errors.

**EV-029 impact on yogurt is MILD (the key finding).** vs run_003: **5/84 grade changes**; score delta median
**0.0**, mean -0.2, range -14.1…+12.0 (35 down / 25 up / 24 ~same). Grade dist C32/B29/D24/E1 → C28/B30/D27/E1.
**Why:** yogurt fat is genuinely low (0/1.5/3%), so the fake-0.5 distortion is numerically minor for the score
(contrast cream-cheese: 0.5 masked real 25–32 g). run_003's grades were *invalid in provenance* but *close in
value*; run_yogurt_004 is the clean citable baseline.

**Reconciliation vs LIVE DEC-005 — downward correction CONFIRMED.** Live manual shelf = A 5 / B 5 / C 3 (top 88/A);
machine run_004 max = **78.7/B (zero A's)**. The manual A's (80–88) are NOT supported on real data — the cleanest
plain bio yogurts cap at ~74–75/B and the **A-ceiling ruling (139A) does NOT restore A**. (Live shelf also carries
non-dairy soy/coconut rows the dairy_protein run doesn't cover 1:1 → plant-pool decision needed at re-author.)
Every delta documented in `reconciliation_143_run_yogurt_004_findings.md`.

**Guards honored:** engine unmodified; **no live frontend touched** (only intermediates re-scored); DEC-005 still
live; no frozen/published score changed.

**DoD: data gates MET; two human gates remain before the live swap** (this is why I do NOT swap):
1. **Product Owner go-live** — accept retiring DEC-005 + the corrected A→B shelf (overwrites a live shelf; hard to reverse).
2. **Content/Design re-author** — insight lines/prologue to the new B-capped shelf + plant-pool decision; 15–20s comprehension test.
Then Data replaces `yogurts_frontend_v1.json` (root + bari-web sync) and retires DEC-005.

**Proposing RETURNED.** Only the Central Controller records CLOSED. The clean baseline (run_yogurt_004) is ready
to freeze; the live swap is correctly gated on PO go-live + Content/Design.

---

## Return block — LIVE SWAP SHIPPED (data-agent, 2026-06-02) — step 3c complete

**Both human gates cleared, then executed the swap.** 3a Product go-live APPROVED (drop+defer ruling on
soy/coconut); 3b Content re-author DELIVERED (`reports/content_reauthor_143_run_yogurt_004.md`: B-capped
prologue + 11 insight lines). Engine UNMODIFIED; no score changed.

**What shipped:**
- **Factory artifact:** `02_products/yogurt_system/yogurts_frontend_v2.json` (built by repeatable
  `build_yogurts_frontend_v2.py` straight from run_yogurt_004 traces) — 11 dairy products, score-descending,
  B-capped (max **79/B** displayed, zero A), 9 verified / 2 partial.
- **Live swap (matches maadanim/hummus pattern):** copied to
  `bari-web/src/data/comparisons/yogurts_frontend_v2.json`; repointed both importers
  (`yogurts-comparison-page-data.ts`, `yogurts-shelf-filters.ts`) v1→v2; v1 JSON kept (orphaned) for rollback.
- **Prologue re-authored** in `yogurts-comparison-page-data.ts` to the B-capped shelf (3b §3; two numbers
  aligned to the rounded ScoreChip: 78.7→79, "71 עד 75"→"72 עד 76"). **dairy-free lens retired** (zero members
  after soy/coconut drop).
- **3a soy/coconut ruling applied:** dropped (run_yogurt_004 contains zero plant-base products); plant yogurt
  deferred to a dedicated plant run.

**Reconcile-check (all green):** 11/11 score+grade match run_yogurt_004 traces (0 mismatch); no orphan ids;
Hebrew coverage 100%; no stale-A / old-anchor lines; clusters plain4/greek2/high-protein3/flavored2.

**Verification:** `tsc --noEmit` EXIT 0; `validate-corpus` **0 errors** (22 non-blocking warnings — §2.4/§2.5 are
the expected consequence of the approved technical-only expansion; §2.8 flags Content's verbatim token 'נקי' in
yog-009 — surfaced to Content, warning-only); `next build` green, **/hashvaot/yogurts** prerendered (33/33 pages).

**DEC-005 RETIRED** in `decisions/decisions.json` (status→RETIRED, retired_at 2026-06-02, retirement_note);
dashboard regenerated. The live shelf is now reproducible/authoritative.

**Known follow-ups (non-blocking, deferred):** (1) interpretive expansion copy (positiveSignals/limitingFactors/
bottomLine) + `unknowns[]` disclosure — deferred by 3b, clears §2.4/§2.5; (2) Content to rule on 'נקי' (§2.8);
(3) dead-but-stale fallback `YOGURTS_INSIGHT_LINES` in `featured-yogurts-intelligence-card.tsx` (unreachable —
products non-empty — but references retired framing); (4) dedicated plant-yogurt run (soy/coconut).

**Proposing RETURNED → ready for Controller CLOSED.** Live swap shipped and verified; only the Central
Controller records CLOSED.
