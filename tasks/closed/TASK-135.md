---
id: TASK-135
title: "run_yogurt_002: real-product yogurt run + reconcile (retire DEC-005 manual-MVP debt)"
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Not necessary for now"
blocker: "Committed non-blocking follow-up to DEC-005; deferred until post-launch / capacity frees. Not started - opened for visibility per the 128E (DEC-003 Amendment A) precedent."
depends_on: []
blocks: []
category_id: null
summary: >
  Real-product yogurt run via category-factory (BSIP0 Shufersal scrape -> BSIP1 -> BSIP2), then reconcile + score-freeze the displayed shelf to retire the DEC-005 manual-MVP provenance exception. Non-blocking; yogurts is already LIVE.
---

# TASK-135 — run_yogurt_002: real-product yogurt run + reconcile (retire DEC-005 manual-MVP debt)

## Update 2026-06-01 (TASK-135A executed) — stays BLOCKED

TASK-135A ran the full real BSIP0→BSIP2 cycle (run_yogurt_002, 46 real OFF SKUs, engine 0.4.0
unmodified). **Verdict NO-GO: DEC-005 cannot be retired with available data.** Root cause:
OFF Israeli yogurt **ingredient coverage = 0%**, and yogurt scoring is ingredient-driven — the
run is 48% INSUFFICIENT, 0 grade-A, ceiling 75/B, and inverts the displayed shelf's logic.

**This task remains BLOCKED** (not closeable). It unblocks only when a real-product source with
**ingredient lists + Hebrew names** exists (authenticated retailer scrape, e.g. a future
run_yogurt_003 — OFF is insufficient). Evidence + exact spec:
`02_products/yogurt_system/reports/reconciliation_135a_findings.md`. Yogurts stays LIVE on the
manual-MVP shelf under DEC-005; this is governance debt, not a launch gate.

## Update 2026-06-01 (run_yogurt_003 executed, Shufersal) — stays BLOCKED, blocker RECLASSIFIED

Ran the full real BSIP0→BSIP2 cycle from **Shufersal** (88 SKUs, engine 0.4.0 unmodified). The
**run_yogurt_002 data blocker is RESOLVED**: ingredient coverage 0%→90%, INSUFFICIENT 48%→**0%**,
NOVA now differentiated (2/3/4), Hebrew names + barcodes + real ingredient panels. Source GO confirmed.

**Verdict: 🟡 NO-GO to retire DEC-005 in this run** — but the blocker has *changed kind*. The machine
run is data-complete yet scores the category much lower (median 57 vs manual 72, **0 grade-A**, ceiling
78/B) because, reading real ingredients, the engine sees added sugar / modified starch / stabilizers
(60% NOVA 4). A real ingredient-bearing corpus exposed three calibration gaps the manual shelf hid:
(1) **router** mis-routes 19% (flavored→dessert, crunch→cereal, "יווני" olives false-positive);
(2) **enricher** detects 0/88 cultures (Israeli label vocab `חיידק פרוביוטי`/`ביפידוס`/`BIFIDUS`/`תרבית`
not in `FERMENTATION_TERMS`) → the yogurt-defining positive is never credited; (3) **dairy A-ceiling**
is a Nutrition/Product philosophy call (is mainstream Israeli yogurt's true ceiling B?).

Old unblock condition ("an ingredient-bearing source exists") is **CLOSED**. New unblock = those 3
scoped, governed fixes + re-run, then editorial/QA before a machine shelf can replace DEC-005. DEC-005
stays; yogurts remains LIVE on the manual shelf. No live scores changed; no frontend dataset shipped.
Evidence: `02_products/yogurt_system/reports/reconciliation_135_run_yogurt_003_findings.md`.
Run preserved non-authoritative: `02_products/yogurt_system/bsip2_outputs/run_yogurt_003/`.
