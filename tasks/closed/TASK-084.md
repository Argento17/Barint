---
id: TASK-084
title: Command Center v3 self-healing task state
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on:
  - TASK-083
blocks: []
category_id: null
summary: >
  Designed + implemented v3 hybrid task-state model. Generator now scans task
  returns and emits PHANTOM_TASK / CLOSURE_DRIFT / SNAPSHOT_DRIFT alerts; added
  check_drift.py watchdog; unified the active-task definition. Delivered
  command_center_v3_design.md and command_center_v3_migration.md.
---

# TASK-084 — Command Center v3 Self-Healing Task State

Hybrid model (Option C): registry authoritative for intent, returns authoritative
for proof, generator reconciles and alerts on drift. Success criterion met — a
deliverable for a task with no registry file is auto-detected as PHANTOM_TASK.
