---
id: TASK-118
title: Comparison UI Reference v2 implementation roadmap
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on: [TASK-111]
blocks: []
category_id: null
summary: >
  Implementation roadmap for Comparison UI Reference v2 (no implementation, no
  redesign). Four phases: Phase 0 v1-safe promotions (#6 confidence promote+gate,
  #8 disclosure de-dup, relativity) → Phase 1 v2 core (#1 density, #2 metric block
  protein+additives only, #5 rowReason, #7 expansion, #9 responsive table) →
  Phase 2 nav chrome (#3 band rail, #4 dividers, histogram) → Phase 3 base_pct
  completion (deferred on new main-ingredient extraction pipeline). base_pct
  removed from Phase 1 per TASK-111. VM deps, 5 downstream blockers, category
  migration order (hummus→maadanim→snacks→yogurts→bread→milk), pilot = hummus.
  Flagged: "TASK-106 decision" input not locatable; TASK-098/DEC-002 govern.
  Accepted and CLOSED by Central Controller 2026-05-31.
---

# TASK-118 — Comparison UI Reference v2 implementation roadmap

Frontend roadmap deliverable consuming the TASK-098 accepted v2 direction
(`handoff/comparison-v2-spec.md`) and the TASK-111 data-dependency readiness
verdict. Phased plan, VM dependencies, blocker list, category migration order,
and hummus pilot recommendation. Roadmap only — no production code modified.

Artifact (website repo): `bari/handoff/comparison-v2-implementation-roadmap.md`

Accepted and CLOSED by the Central Controller on 2026-05-31.
