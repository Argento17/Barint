---
id: TASK-395A
title: De-chain: fix dedup comparator (stated_pct must beat position-weight)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-25
depends_on: []
blocks: []
category_id: null
summary: >
  matrix_signal extract_all_markers dedup keeps position-weight over a stated_pct when pos_weight is numerically larger (pos_weight(3)=0.68 beats stated 40%); must prefer stated_pct unconditionally. Real but harmless: 0 grade/gate changes corpus-wide (481180 25.5->33.2, stays F). Fix before de-chain deploy. Src: QA a1eb64c1adaf91c8b + Data verdict A.
---

# TASK-395A — De-chain: fix dedup comparator (stated_pct must beat position-weight)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
