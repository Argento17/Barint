---
id: TASK-291
title: Backfill _meta.run_id on the 7 frontend comparison JSONs missing it (release platform Phase 1 traceability)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  C2/DeepSeek, round-2 corrected (P151), orchestrator-verified against traces. Backfilled run_id only
  where the run REPRODUCES the page scores: cereals_v2=run_cereals_008 (3/3 exact) + granola_v1=
  run_cereals_008 (rounding-consistent) — KEPT. snacks_v2 + yogurts_v3 = REVERTED to absent (run_id:None):
  no run reproduces their scores (yogurts_v3 barcodes exist in run_yogurt_006 but scores differ 87 vs 92.6;
  snacks_v2 fails run_snack_bars_001), so left honestly ambiguous rather than fabricating provenance.
  Scope clean: only the 2 kept JSONs carry a +run_id line; reverts touch only _meta.run_id. cheese_v3 +
  hummus_v5 (+ the 2 reverted) remain run_id:None — unrecoverable provenance, surfaced honestly in the manifest.
  Lesson logged: C2 = zero-inference only (memory c2_grunt_only_no_inference; skill C2 line sharpened).
changes_requested: >
  Round-1 (C2/P151) matched run_id by barcode-presence, not score-provenance. Orchestrator-verified:
  cereals_v2→run_cereals_008 ✅ and granola_v1→run_cereals_008 ✅ (scores match) — KEEP; but
  snacks_v2→run_snack_bars_001 ❌ (page 60 vs trace 56.7; 57 vs 68.0) and yogurts_v3→run_yogurt_006 ❌
  (page 87 vs trace 92.6) are WRONG (barcodes present but scores don't reproduce). Round-2 rule: assign
  run_id ONLY to the run whose traces reproduce the page scores (|Δ|<0.6, ≥80% of products), else REVERT
  to absent + report ambiguous. Re-dispatched P151 (in-lane retry).
summary: >
  live_state manifest exposed 7 pages with run_id:None (cereals_v2, cheese_v3, granola_v1, hummus_v5, snacks_v2, yogurts_v3, + 1). Backfill _meta.run_id from each page's authoritative source run. Mechanical; no score/copy change.
---

# TASK-291 — Backfill _meta.run_id on the 7 frontend comparison JSONs missing it (release platform Phase 1 traceability)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
