---
id: TASK-121
title: Investigate why TASK-120 return did not update the Command Center
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-06-01
depends_on: []
blocks: [TASK-122]
category_id: null
summary: >
  Root-cause why an agent's RETURNED proposal did not surface TASK-120 on the
  dashboard. Finding: no TASK-120.md existed and nothing parses the proposed-
  state block or auto-regenerates the derived dashboard. Documents the current
  manual workflow and what must change. Advisory; no automation built.
---

# TASK-121 — Registry Update Gap Investigation

Traced why TASK-120's return left the Command Center unchanged: the dashboard
is derived solely from C:\Bari\tasks\TASK-*.md, TASK-120 had no file, and the
"Registry Update (proposed)" block is transcript prose that nothing ingests.
Recording state and regenerating the dashboard are manual Controller steps.
Motivated TASK-122 (Task Creation Protocol).

> Retroactively registered at RETURNED by the Central Controller (2026-05-31)
> per task_creation_protocol_v1 §3. Deliverable is the return itself (advisory;
> no files modified). Awaiting review; not yet accepted.
