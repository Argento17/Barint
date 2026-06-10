---
id: TASK-122
title: Define Task Creation Protocol
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on: [TASK-121]
blocks: []
category_id: null
summary: >
  Define the process for opening a task: who creates TASK-NNN.md, at what
  moment, the minimum required frontmatter fields, how the dashboard sees a
  newly opened task, and how Registry Work is distinguished from Conversation
  Work at creation time. Process definition only; no automation. Delivered
  01_framework/operations/task_creation_protocol_v1.md.
---

# TASK-122 — Define Task Creation Protocol

Entry-gate protocol complementing registry_protocol_v1 (which covers reporting
and closing). Closes the gap traced by TASK-121: a task must be registered at
the instant it is opened, or the work is invisible to the Command Center.

Deliverable: `01_framework/operations/task_creation_protocol_v1.md`.

> Retroactively registered at acceptance (Central Controller approved
> 2026-05-31). Per task_creation_protocol_v1 §3, work delivered before a file
> existed is registered by the Controller at the state reflecting reality —
> here CLOSED, since it was approved on return.
