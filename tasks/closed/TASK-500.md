---
id: TASK-500
title: Harness bug — multi-shelf single-process rescore_all.py cross-contaminates via unreloaded module-level env reads
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-05
close_reason: >
  Harness-only robustness fix, orchestrator-verified NEUTRAL (2026-07-05 unattended run). Root cause
  confirmed: rescore_all.py reloaded only score_engine; nova_proxy(2)/signal_extractor(3)/router_v2(1)/
  constants(1) = 7 module-level os.environ reads stayed stale across shelves. Fix = per-shelf subprocess
  isolation via new _score_shelf_worker.py (spawns fresh process, applies BARI_* flags BEFORE any import).
  Commit 83f12228 on fix/task500-rescore-isolation (worktree C:\bari_wt_t500, off origin/master c6993b48).
  NEUTRALITY verified: (1) C0 validate_return --json PASS, all neutrality claims carry distribution markers,
  both artifact sha256 match; (2) diff = +239/-27 across ONLY the 2 harness .py files, orchestrator scanned
  it — subprocess/env plumbing only, ZERO scoring-formula/threshold change; (3) worker imports the real
  score_engine (line 52) so each subprocess IS the trusted single-shelf path → batch==isolated is neutral by
  construction; agent reports 1088/1088 zero deltas + sentinel 5718038 now 22.0/E in batch (was 20.6/E
  contaminated); (4) worktree clean — no live score/frontend JSON written. NOT pushed — internal-fix merge to
  master queued for supervised morning (unattended never-push rule). No published score touched.
depends_on: []
blocks: []
category_id: null
summary: >
  Found during TASK-496 (honest escalation, PRE-EXISTING — reproduced on unmodified origin/master, NOT
  caused by TASK-496). rescore_all.py reloads ONLY score_engine.py (importlib.reload ~line 300-303); but
  nova_proxy.py, signal_extractor.py, router_v2.py, trace_writer.py read os.environ at MODULE level and are
  imported via `from X import Y` inside make_score_one() — Python no-ops the re-import if already cached. So
  in a MULTI-shelf single-process run (rescore_all.py with NO --shelf filter), an earlier shelf's flag
  freezes those modules' state and leaks into later shelves. Reproduced: brined_cheeses (alphabetically
  first, config BARI_RECAL_P0=on) freezes nova_proxy.RECAL_P0_ON=True; cakes (wants BARI_RECAL_P0=off) then
  scores under stale RECAL_P0=on, moving cakes barcode 5718038 22.0/E → 20.6/E in that shared-process run
  only. Single-shelf subprocess runs are UNAFFECTED (the trusted reproduction path).
---

# TASK-500 — multi-shelf rescore reload isolation bug (from TASK-496 finding)

## Why it matters
- LIVE scores are NOT wrong: they were produced correctly, and single-shelf reproduction is clean (TASK-496
  proved 167/167 zero-movement via per-shelf isolated runs). So this is NOT a live-score defect.
- BUT the "rescore all shelves in one process" path (rescore_all.py with no --shelf) is UNRELIABLE — it can
  silently cross-contaminate flags between categories. This is a traceability/robustness risk for anything
  that batch-rescores (e.g. a spine_flip that re-scores every category), and a latent trap for future work.

## Deliverable (investigation-first; scoring-harness correctness, do not rush)
1. Confirm the reload gap: which env-reading modules are NOT reloaded alongside score_engine (candidates:
   nova_proxy, signal_extractor, router_v2, trace_writer). Cite file:line of each module-level os.environ read
   + the reload site (~rescore_all.py:300-303).
2. Fix so a multi-shelf run isolates per-shelf flag state — either reload ALL env-dependent modules together,
   or (safer) run each shelf in a subprocess, or thread flags as explicit params instead of module-level env.
   Choose the least-invasive correct option; explain the tradeoff.
3. HARD GATE: prove single-shelf path stays 167/167 zero-movement AND the multi-shelf path now matches the
   per-shelf isolated results (batch == isolated). If any live-displayed score would move → STOP + finding
   (tripwire-1 / owner).

## Guards
- Scoring-harness correctness — treat like TASK-496 (neutrality proof is the safety). Base off origin/master.
- Do NOT change any published score. Internal harness fix → orchestrator may merge if fully neutral.

## Return: 5-part + reload-gap map + neutrality proof (single-shelf still 0-move + batch==isolated) + Return
Contract JSON. Propose RETURNED.
