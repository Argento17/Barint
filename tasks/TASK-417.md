---
id: TASK-417
title: Rendered-review DATA fixes: sort cereals rows by score, source real hummus brands, apply discard rule to cookies_coffee partial-data products
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Owner rendered-review batch 2026-07-01 (data items #1,#7,#4): (1) sort cereals_frontend_v2.json products by score desc so band dividers line up; (7) populate hummus_frontend_v5.json brand from the REAL hummus corpus/scrape (never invent; null if genuinely absent); (4) cookies_coffee_frontend_v2.json — identify products whose material nutrition fields are missing (confidence_label_he partial/missing) and DISCARD them per [[missing_data_discard_rule]] instead of showing a partial-analysis disclaimer; propose the discard list for confirm. Data/JSON only; no score change; OFF-ban; staging.
---

# TASK-417 — Rendered-review DATA fixes: sort cereals rows by score, source real hummus brands, apply discard rule to cookies_coffee partial-data products

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
