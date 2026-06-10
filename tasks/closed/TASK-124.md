---
id: TASK-124
title: Add one-click task action buttons to Command Center
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  State-aware one-click task actions on the Command Center so the Central
  Controller can change a task's lifecycle state from the dashboard. Local-only
  serve.py POST /api/action validates the task id, current state, and requested
  transition; rewrites ONLY the target TASK-NNN.md YAML frontmatter (registry
  stays source of truth); appends to task_action_audit.log; runs
  generate_dashboard.py; the page refreshes. Adds no lifecycle states and no
  product/category code.
---

# TASK-124 — Command Center one-click task actions

Frontend tooling deliverable: state-aware action buttons on the operational
dashboard (`command_center_v4.html`) backed by a local-only `POST /api/action`
endpoint in `serve.py`. On click the server validates the task id, the current
state, and the requested transition; rewrites only the YAML frontmatter of the
target `TASK-NNN.md`; appends to `task_action_audit.log`; runs
`generate_dashboard.py`; the page re-fetches the regenerated JSON.

Action model (no new lifecycle states — the existing five only):
- IN_PROGRESS → Mark Returned / Close / Block
- RETURNED → Accept / Request Changes
- CHANGES_REQUESTED → Resume / Close
- BLOCKED → Resume / Close

`completed_at` is added on any transition to CLOSED; a reason is required for
Block, Request Changes, and Close (and recorded in the audit log + frontmatter).

Artifacts (no website-repo changes):
- `C:\Bari\05_command_center\serve.py` — /api/action backend, frontmatter editor, audit, allow_reuse_address
- `C:\Bari\05_command_center\command_center_v4.html` — state-aware action buttons + 501-recovery messaging
- `C:\Bari\05_command_center\task_action_audit.log` — local audit trail (created on first action)

> Retroactively registered at RETURNED by the Central Controller (2026-06-01)
> per `task_creation_protocol_v1` §3 — the action-model work was delivered across
> several iterations before a registry file existed, the same invisible-work gap
> TASK-121 traced. Awaiting review; not yet accepted.
