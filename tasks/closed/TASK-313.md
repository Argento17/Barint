---
id: TASK-313
title: Juices NOVA fix (RT-3) — correct stale nova=3 on 5 fresh-squeezed grade-A juices before push
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-310, TASK-311]
blocks: []
category_id: null
close_reason: >
  P165/C1-GROK, orchestrator-verified against juices_frontend_v3.json. All 5 fresh-squeezed grade-A juices (7290003009640,
  7290004030100, 7290013153395, 7290110114886, 7290110114893) now novaGroup=1 (confirmed single-ingredient 100% juice via
  ingredients + BSIP1 additive_count=0; matches peer 7290000525969). 0 grade-A products carry nova=3 (was 5). Scores+grades
  vs staging: 0 mismatch (P165 touched only novaGroup; the other working-tree diff lines are P163's prior assembly, already
  verified in TASK-310). Count 21. No OFF, no fabrication. Reversible, not pushed.
summary: >
  Red-team RT-3: 5 single-ingredient 100% fresh-squeezed grade-A juices (7290003009640, 7290004030100, 7290013153395,
  7290110114886, 7290110114893) carry stale novaGroup=3 (ultra-processed-lite) — definitionally wrong (squeezed single-
  ingredient juice = NOVA 1) and internally inconsistent (peer squeezed juices already show nova=1). Inherited from a legacy
  run; shelf-relative rescore did not recompute NOVA. Fix = set novaGroup=1 where ingredients confirm single-ingredient 100%
  juice, else null (never invent, never OFF). Display-only; scores/grades MUST stay byte-identical. Route C1-GROK (P165),
  edit only juices_frontend_v3.json. Reversible, no deploy.
---

# TASK-313 — Juices NOVA fix (RT-3)

See `tasks/prompts/P165_juices_nova_fix.md`.
