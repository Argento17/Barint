---
id: TASK-168F
title: Row layout — let the collapsed verdict display fully (raise clamp + row height)
owner: frontend-agent
status: CLOSED
priority: HIGH
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "Removed line-clamp-2 from the verdict <p> (comparison-row.tsx:120); the row grid has no fixed height so it grows to fit, image/name/metric/chip stay aligned. Live-verified 0 line-clamp-2 in markup, full verdicts render no truncation. Other categories' single-line insightLine/rowReason branches keep truncate (unchanged). tsc+lint clean. Owner confirmed readable."
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
summary: >
  Verdict model approved directionally; the 2-line clamp (comparison-row.tsx:120 line-clamp-2) + fixed row height truncate the 2-sentence verdict with '...'. Let the row grow to show the full verdict (≈3 lines) without truncation, keeping image/name/metric/chip alignment + mobile. Shared component (applies to rollout). Display-only.
---

# TASK-168F — Row layout — let the collapsed verdict display fully (raise clamp + row height)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
