---
id: TASK-298
title: Quick re-score trigger — generic one-command re-score of all configured shelves (rescore_all) built on the proven pipeline_e2e chain
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  Quick re-score trigger BUILT + orchestrator-verified (Data Agent C1-Sonnet/P159, after 2 C1-GROK attempts P157/P158
  hit the retry limit; lane-up per escalation). Owner ruled CANONICAL RE-BASELINE: rescore_all.py freezes each shelf's
  authoritative D7-blessed shelf-stats into config + applies them deterministically; score moves vs live are EXPECTED
  reviewable output, not failures. ORCHESTRATOR INDEPENDENTLY VERIFIED all hard gates (not on the agent's word):
  (1) DETERMINISM — re-ran cereals 2x, score digest 4302bc65d6501ce9 stable; full re-run exit 0.
  (2) MILK INVARIANT — C10 PASS 9/9 (20/20 milk products each, Δ0 under MILK_CANONICAL_FLAGS vs committed run_005_headpin);
  rescore_all.py:369-449 is a genuine gate; milk also not in any config (page untouched). P158's "milk Δ2.8" root-caused +
  fixed = C10 was scoring milk under shelf flags (RECAL_P0=on); now isolated under milk-canonical flags.
  (3) OFF=0 in all 9 staging pages. (4) engine `git diff proto_v0/src/` EMPTY; bari-web diff EMPTY; staging-only.
  Frozen invariants hold: milk Δ0, snacks max=70.0/B (no A), cereals+juices reproduce live 0/0. Engine-drift claim
  (P158) DISPROVEN (engine identical to f1d1275e). Deliverables: rescore_all.py + 9 config scoring blocks +
  _rescore_staging/rebaseline_delta_report.md (128 score / 29 grade moves total — the review artifact).
  Pre-existing (not introduced): hard_cheeses 28/30 (2 OFF products excluded, documented launch blocker).
  NEXT (separate, downstream): Nutrition + red-team review of the deltas -> owner deploy. Uncommitted (owner-gated).
depends_on: [TASK-296]
blocks: []
category_id: null
summary: >
  Build the release-platform core: one generic command that re-scores ALL configured shelves in one go. For each configs/*.json (excl _generated_*): read BSIP1 corpus -> run the current scoring engine (extract_signals/classify/nova/scope/score/assemble_trace, the proven pipeline_e2e chain) -> fresh BSIP2 traces -> generate_page -> verify score==trace + OFF=0 + gates -> diff vs live. NO re-scrape (reads existing BSIP1; quick). Output to STAGING, never overwrite live. Deterministic, OFF-ban enforced, no deploy. milk excluded (no config = frozen exception).
---

# TASK-298 — Quick re-score trigger — generic one-command re-score of all configured shelves (rescore_all) built on the proven pipeline_e2e chain

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
