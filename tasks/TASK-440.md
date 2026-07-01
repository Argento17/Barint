---
id: TASK-440
title: Re-flow cookies_coffee to current engine (9 movers, 1x D->C upward)
owner: data-agent
status: BLOCKED
blocker: DATA-INTEGRITY BUG — cookies_coffee corpus record for 7290119043149 is TRUNCATED (ingredients cut off at 'קמח חיטה לבן ('), dropping E450/E500 + hydrogenated fat. Truncated parse -> 0 additives -> NOVA-2 -> false 55.0/C. Complete parse (cakes corpus) = NOVA-4 -> 47.7/D (matches live). The ONLY grade move (D->C) is a corpus artifact, NOT a real improvement. HOLD re-flow; live D is correct. FIX: re-scrape/repair the truncated record + run an ingredient-completeness sweep on the whole cookies_coffee corpus before any re-flow. Content draft for this product discarded (based on corrupted data).
priority: MEDIUM
created_at: 2026-07-01
depends_on: [TASK-436]
blocks: []
category_id: null
summary: >
  cookies_coffee mostly sub-point drift + one +7.3 upward grade correction (7290119043149 D->C). Rescore -> copy reconcile -> gates -> deploy.
---

# TASK-440 — Re-flow cookies_coffee to current engine (9 movers, 1x D->C upward)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## STAGED (2026-07-01, orchestrator) — rescore done
rescore_all --shelf cookies_coffee: 9 score-moves, **1 grade move 7290119043149 D->C (upward +7.3)**. gate PASS, score==trace OK. Low-stakes, single upward correction. Next: copy_stage -> author (1-few products) -> Adversarial QA -> deploy. Cleanest of the 3; proceed once cakes pattern confirmed.
