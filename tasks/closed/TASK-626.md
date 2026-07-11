---
id: TASK-626
title: Low-evidence triage: classify the 44 <50%-evidence products (re-scrapable vs genuinely-missing)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
close_reason: "TRIAGE delivered + committed b2456a16. 44/44 low-evidence products RE-SCRAPABLE, 0 genuinely-missing: 17 never-captured (yohananof), 24 (cookies_coffee) capture-exists-but-matcher-missed, 3 collision/parser edge. Flagged cross-category GTIN-collision bug. Spawns the capture-matcher fix lane (kills 24) + re-scrape-17 follow-up."
summary: >
  For the 44 products with evidenceCompleteness <50%: classify each as (a) re-scrapable (fields exist on source, capture missed them) or (b) genuinely-missing (per missing-data-discard rule, stays null). Produce the triage list + the re-scrape target set. Diagnostic, minimal writes.
---

# TASK-626 — Low-evidence triage: classify the 44 <50%-evidence products (re-scrapable vs genuinely-missing)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
