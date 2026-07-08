---
id: TASK-525
title: signal_extractor.py whitespace-fragility: internal-whitespace normalization needed in ingredient matcher (systemic, all categories)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Nutrition-recommended systemic follow-up (surfaced during TASK-515 spoonable rescore): matcher uses per-term literal variants instead of internal-whitespace normalization, causing real ingredient signals to hide behind scrape whitespace artifacts (e.g. space-split words). Harden across ALL categories with Nutrition+Product co-sign on the fix design. NOT a tapioca-fix duplicate -- this is the general whitespace-tolerance gap; tapioca-fix (TASK closed this session) was a different, source-word-tolerance gap in the same file family.
---

# TASK-525 — signal_extractor.py whitespace-fragility: internal-whitespace normalization needed in ingredient matcher (systemic, all categories)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
