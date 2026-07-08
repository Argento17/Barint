---
id: TASK-526
title: bari-grade-badge.tsx legacy-import boundary violation: canonical comparison-row.tsx imports a quarantined component
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced during TASK-515A drinkable wire+render verification: src/components/shared/comparison-row.tsx imports bari-grade-badge.tsx, one of the 4 files explicitly named in the Frontend Agent's legacy-quarantine list ('do not import into canonical components'). Both bari-grade-badge.tsx and the parallel score-chip.tsx correctly read BARI_COMPARISON_TOKENS.gradePalette so no rendering risk today, but the import boundary itself is a pre-existing violation. Pre-existing, not introduced this session.
---

# TASK-526 — bari-grade-badge.tsx legacy-import boundary violation: canonical comparison-row.tsx imports a quarantined component

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
