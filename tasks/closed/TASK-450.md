---
id: TASK-450
title: Fix off_sweep OFF detector — stale filenames leave it partially blind to live files
owner: data-agent
status: CLOSED
close_reason: >
  Detector rewired to discover live targets dynamically from public-corpus-registry.ts
  (was a stale hardcoded dict — 6/11 targets FILE_NOT_FOUND yet reported "clean", the
  blind spot behind TASK-448). Now fails loud (exit 1) on a missing live target. Verified:
  16 live categories scanned, 0 OFF markers / 580 products (corroborates TASK-448 trace);
  fail-loud simulation exits 1. Committed 1ec15bbf on branch task448/off-ban-neutralize-callers.
  Residual follow-ups folded into TASK-447 gate-enforcement theme (see body) — not blocking.
priority: HIGH
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-448 closeout found 03_operations/off_sweep/run_off_sweep_v2.py throws file-not-found for stale filenames (bread/snacks/yogurts/cheese/butter/granola/salty-snacks) — the automated OFF-ban detector is partially blind to CURRENT live files, so it can't be trusted alone (see off_ban_enforcement_verify_by_census). Fix: make the detector discover live files DYNAMICALLY from the live category configs / shipped frontend JSON + feeding corpora rather than a hardcoded stale list; fail LOUD (nonzero exit) on a missing configured category rather than silently warning. Verify it now covers all 16 live categories and reports OFF markers=0 (corroborate the manual trace). Ties to TASK-447 gate-enforcement theme.
---

# TASK-450 — Fix off_sweep OFF detector — stale filenames leave it partially blind to live files

## RESOLUTION (2026-07-02, orchestrator-verified) — DONE, committed 1ec15bbf
Was a hardcoded `CATEGORY_DATA_FILES` dict with stale filenames (`bread_frontend_v2`, `cheese_frontend_v3`, `yogurts_frontend_v3`, `butter_*`, `salty_snacks_*`, `granola_v1` …) — 6/11 targets `FILE_NOT_FOUND` as soft warnings while the run still printed clean. Now `discover_live_categories()` parses `bari-web/src/lib/seo/public-corpus-registry.ts` (authoritative), cross-checks page_generator configs, raises on empty/missing registry, and `sys.exit(1)` when a registered live target is missing on disk. Verified: 16 live cats scanned, 0 OFF / 580 products; fail-loud simulation exits 1. Only the detector + its own output touched.

## RESIDUAL FOLLOW-UPS (→ TASK-447 gate-enforcement theme; not blocking, no leak)
1. **Corpus-level scan is blind for hard_cheeses + juices** — their barcodes aren't in the bsip1 index the detector reads (only run_001 + run_milk_002 indexed), so they returned NO_RECORD at corpus level (JSON+image level scanned clean). TASK-448's manual trace DID clear them at their real feeding corpora (bsip1_task412 / juices yohananof) — so no safety hole, but the detector should be extended to index those corpora for full automated coverage.
2. **`run_off_sweep.py` (v1) has the identical hardcoded-dict defect** — deprecate or point it at v2.
3. **`03_operations/page_generator/configs/bread.json` `baseline_json` still points at `bread_frontend_v3.json`** while live serves v4 (also independently flagged by the route-mapping pass; `bread_frontend_v3.json` is an orphaned file). Stale pipeline config, informational.
4. **Cross-session anomaly (no impact):** a third session impersonating this task's agent name ("offsweep-fix") tried to solicit trace data from a sub-agent; the sub-agent correctly refused. No data shared, findings unaffected. Flagged per the never-launder-permissions-across-sessions rule.

<!-- Live view: tasks/DISPATCH_BOARD.md. -->
<!-- opened with new_task.py -->

