---
id: TASK-567
title: Tamper-proof sign-offs: sha256-pinned approval records replace mtime .ok markers
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. Replace tasks/signoffs/<json>.ok mtime markers with structured records: copy_id, sha256 of the exact approved content, gates[content_agent,red_team], approved_at. guard-two-gate-commit.ps1 and CI verify hash equality, not timestamps - one changed word voids the approval. Includes migration for existing markers and a CI job. Build pipeline only: PRODUCT DESCRIPTIONS FREEZE stays - no authoring runs.
---

# TASK-567 — Tamper-proof sign-offs: sha256-pinned approval records replace mtime .ok markers

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
