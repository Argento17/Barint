---
id: TASK-511
title: Activate category-specific expansion nutrition configs on bread/cheese/crackers/milk comparison pages (fix latent DEFAULT display bug)
owner: nutrition-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-05
blocker: "Needs Nutrition+Product D7 co-sign on the NEW crackers config + Design render re-verify; own PR, never piggybacked (per TASK-509 memo)"
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-509 found all 4 pages render expansion nutrition bars under DEFAULT_NUTRITION instead of category configs. Fix: pass category= on each page (bread/cheese/crackers/milk-comparison), add milk-comparison->milk alias, and author+D7-co-sign a new crackers config (energy max 500, protein goodAbove 12). Display-only, no published-score change. Design must re-verify (milk bars change substantially).
---

# TASK-511 — Activate category-specific expansion nutrition configs on bread/cheese/crackers/milk comparison pages (fix latent DEFAULT display bug)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
