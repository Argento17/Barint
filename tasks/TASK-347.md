---
id: TASK-347
title: Phase 2+3 WS-Data remediation: fix parsing gaps for the dropdown (clean malformed, compute rank, re-derive nulls from scrape)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-19
depends_on: [TASK-345]
blocks: []
category_id: null
summary: >
  Per TASK-345 audit: clean 5 malformed ingredient strings; compute+bake rank/categoryTotal for all 407; investigate raw bsip0/bsip1 scrape and re-derive systematic null sugar/sodium + absent d4_additives (milk/juices) WHERE PRESENT; report genuinely-unrecoverable (stays missing per rule). OFF banned, no fabrication, staging only, re-run coverage after.
---

# TASK-347 — Phase 2+3 WS-Data remediation: fix parsing gaps for the dropdown (clean malformed, compute rank, re-derive nulls from scrape)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
