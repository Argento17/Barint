---
id: TASK-125
title: Remediate registry drift and add new_task.py opener helper
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Dashboard looks OK"
depends_on: []
blocks: []
category_id: null
summary: >
  Remediate the existing registry drift surfaced by the Command Center (18
  PHANTOM_TASK ids + 2 REGISTRY_UNPARSEABLE files) so the dashboard reflects
  reality, and add a new_task.py helper that writes a schema-correct
  TASK-NNN.md at open time and regenerates — lowering the friction that causes
  invisible-work drift (TASK-121/122). Convention-based; no CI gate, no new
  lifecycle states, no product/category code.
---

# TASK-125 — Registry drift remediation + opener helper

Root-cause follow-up to TASK-124's discovery that the task we were working on
(TASK-124) was itself invisible — the same gap TASK-121 traced and TASK-122's
Task Creation Protocol was written to close, but which nothing enforces.

Scope:
- **Tier 1 — remediate the backlog:** repair the 2 unparseable files (TASK-029,
  TASK-032) and create registry records for the 18 phantom ids at the state that
  reflects reality (per `task_creation_protocol_v1` §3 retroactive remediation),
  each with a retroactive-registration note citing the deliverable it was derived
  from.
- **Tier 2 — prevention:** add `C:\Bari\05_command_center\new_task.py` so opening
  a task is one command (schema-correct frontmatter at IN_PROGRESS + regenerate),
  making "register at open" frictionless.

Out of scope (deferred, separate decision): Tier 3 automation (return-block
ingestor / file-watcher), which would reverse the protocol's deliberate
convention-over-CI choice.
