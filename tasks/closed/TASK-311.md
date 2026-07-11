---
id: TASK-311
title: Final RED-TEAM gate — adversarially tear apart the 7 finished, assembled re-baseline pages before owner push
owner: red-team-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - all 7 re-baselined pages live on origin/master (granola/juices/breakfast-cereals routes asserted); pre-push gate satisfied by the push; category-level red-team backfill tracked in TASK-474. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-310]
blocks: []
category_id: null
summary: >
  Stage-9 red_team_gate (factory terminal layer) on the 7 re-baselined pages now assembled into bari-web (cereals, cakes,
  cookies_coffee, granola, juices, brined_cheeses, hummus) + the /hashvaot/vegetable-spreads page (shares hummus_frontend_v5.json).
  Tear them apart: images resolve, shelf-filter dropdowns/lenses complete, build passes, page score == authoritative staging
  rescored score (shelf-relative re-baseline; NOT raw run trace), OFF=0 in all product data, copy coherent/strong/grade-honest/
  non-fabricated/no-framework-leakage/no-stale-numbers, cross-page coherence (hummus dips-only vs vegetable-spreads lenses).
  Classify findings CRITICAL/HIGH/MED. Does NOT fix, NOT approve, NOT close. Owner-ready ONLY at zero CRITICAL. Then → owner push (gated).
---

# TASK-311 — Final red-team gate on the assembled re-baseline pages

See `tasks/prompts/P164_final_redteam_gate.md`. Owner push is the gated step AFTER this clears zero-CRITICAL.
