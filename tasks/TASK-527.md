---
id: TASK-527
title: Investigate brined-cheeses 14 + milk 3 score==trace / ingredient-truncation mismatches on LIVE pages
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced incidentally by the validate_comparison_page.py --http instrument fix during TASK-515A: re-running the (now-fixed) go-live battery against LIVE brined_cheeses and milk pages found brined-cheeses has 14 score==trace mismatches and milk has 3 ingredient-truncation flags. Pre-existing, unrelated to yogurt or the instrument fix itself (confirmed the instrument fix only changed image-URL resolution, not score/ingredient logic). Need to determine: stale committed traces vs a real live-page drift. Not yet triaged for severity.
---

# TASK-527 — Investigate brined-cheeses 14 + milk 3 score==trace / ingredient-truncation mismatches on LIVE pages

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
