---
id: TASK-568
title: Derived views: homepage carousel + featured duel generated from comparison JSON at build time
owner: frontend-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. The ~16 hand-maintained featured-*-intelligence-card.tsx components carry scores/counts that silently drift from the served comparison JSON. Replace hand-maintained numbers with build-time derivation from the JSON (single StoryCard-style data shape). Approved copy strings remain inputs (two-gate governed) - only data fields derive. Needs design scoping before build; verify with a derived-vs-JSON parity check that becomes a CI fixture.
---

# TASK-568 — Derived views: homepage carousel + featured duel generated from comparison JSON at build time

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
