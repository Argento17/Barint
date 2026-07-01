---
id: TASK-423
title: W4: Orchestrator durability — dispatch journal+lock+worktree-default, canary/rollback ledger
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-420, TASK-421]
blocks: []
category_id: null
summary: >
  3 parts: (a) append-only tasks/_journal/<run>.jsonl step-log so /orchestrate resumes mid-run (journal-replay, never re-run completed step); (b) dispatch lock serializing dispatch.py + worktree-default for CLI lanes (kills race + tree-wipe hazards); (c) promote.py: staging candidate -> shadow-score vs baseline -> promote to live_manifest only if gates pass, one-command rollback. Promote step stays owner-gated (tripwire-2).
---

# TASK-423 — W4: Orchestrator durability — dispatch journal+lock+worktree-default, canary/rollback ledger

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
