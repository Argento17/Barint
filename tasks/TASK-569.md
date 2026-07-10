---
id: TASK-569
title: Generate page JSON schema from BariProductVM (kill schema lag class)
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. page_output_schema_v1.json is hand-maintained and lagged an owner-approved copy change (TASK-564 false alarms). Generate the schema from the TS view-model at build time (free OSS tooling only), diff against current schema, adopt after review. TASK-564's manual fix lands first; this prevents recurrence.
---

# TASK-569 — Generate page JSON schema from BariProductVM (kill schema lag class)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
