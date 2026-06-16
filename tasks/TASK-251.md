---
id: TASK-251
title: BSIP1 shared data integrity gates — lift macros_plausible + ingredient_text_quality from yogurt builder into bsip1/core; wire BSIP0 validator as Stage-B pre-condition
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  FIX-2: run_yogurt_006 macros_plausible and ingredient_text_quality checks protect only yogurts. Shared bsip1/core has no plausibility gate. Goal: extract these checks into 03_operations/bsip1/core/ and wire the TASK-218 BSIP0 validator as a mandatory pre-BSIP1 call so all category pipelines fail fast on corrupted scrape or parse output.
---

# TASK-251 — BSIP1 shared data integrity gates — lift macros_plausible + ingredient_text_quality from yogurt builder into bsip1/core; wire BSIP0 validator as Stage-B pre-condition

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
