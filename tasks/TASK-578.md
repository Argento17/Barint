---
id: TASK-578
title: Magnesium page has no generated-date source: hardcoded 'updated June 2026' label
owner: data-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-568 scoping finding: magnesium-page-data.ts has no JSON 'generated' field to derive the updated-label from; the card hardcodes a Hebrew June-2026 string that will silently go stale. Add a generated timestamp to the magnesium data source and derive the label like the other cards (comparison-card-stats module).
---

# TASK-578 — Magnesium page has no generated-date source: hardcoded 'updated June 2026' label

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
