---
id: TASK-553
title: build_copy_inputs.py hygiene: code the superlative margin gate + de-hardcode S_VERBATIM
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Two follow-ups surfaced by TASK-550's red-team. (1) superlatives_allowed_policy_v1.md rule 3 (margin >=10% of corpus range over 2nd place) is written but NOT coded; retroactively it would revoke rice-apple's thin lowest_sugar token (0.4g gap on a 26.1g range). (2) S_VERBATIM is a module-level global in the SHARED build_copy_inputs.py hardcoded with the YOGURT category's S-grade barcodes — it leaked phantom s_products into every category's fact sheet _meta. A minimal filter fix was applied; the architecture (per-category data hardcoded in a shared script) violates the uniform-baseline doctrine and needs a real cleanup.
---

# TASK-553 — build_copy_inputs.py hygiene: code the superlative margin gate + de-hardcode S_VERBATIM

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
