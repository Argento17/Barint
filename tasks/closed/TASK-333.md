---
id: TASK-333
title: Publish hard_cheeses: regenerate corrected scores (D->B bug-fix, Nutrition-blessed) + re-author changed-grade copy + Anti-Immunity caveat + 28-count note
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  Page deliverable COMPLETE + committed (orchestrator-verified C0). Corrected scores
  (Nutrition-blessed: old 39/D was an implied-red-label-cap bug; NOVA-2 reclassification
  correct) — 28 products, B24/C2/D2. Copy authored for 19 grade-changed products +
  Anti-Immunity caveat. Stage-9 red-team found 3 CRITICAL + 3 HIGH (null subPool/imageUrl
  render-contract regressions, fabricated Baby Bel sodium, false D-attribution); ALL
  remediated via lanes (render_fields.py subPool fix + overlay-merge display-field carry +
  Baby Bel honest rewrite + trans-fat disclosure) and re-verified: 9/9 findings resolved,
  every HARD gate PASS, npm build green, scores unchanged. Promoted to served
  hard_cheeses_frontend_v2.json. LIVE DEPLOY to bari.digital remains blocked on
  deploy-topology (TASK-314) — not this task's scope.
depends_on: []
blocks: []
category_id: hard_cheeses
summary: >
  Nutrition confirmed the live 39/D was a bug (implied-red-label cap); current-config rescore (NOVA-2 reclassification) is correct. Regenerate served page (staging), re-author copy for the 19 D->B products + category caveat, gate+build, commit. Go-live deploy stays owner-gated/topology-blocked.
---

# TASK-333 — Publish hard_cheeses: regenerate corrected scores (D->B bug-fix, Nutrition-blessed) + re-author changed-grade copy + Anti-Immunity caveat + 28-count note

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
