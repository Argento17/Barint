---
id: TASK-574
title: Strip raw internal fields from 6 served comparison JSONs (_scoring_trace, nutrition_per_100g, duplicate name_he/image_url)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found by TASK-564 shape census: chocolate_bars, chocolate_tablets, cookies_coffee, juices, protein_bars, snacks ship raw build-path fields in consumer-served JSON (internal _scoring_trace {category, protein_g}, raw nutrition_per_100g duplicating expansion.nutrition, duplicate name_he/image_url). Display-neutral cleanup of governed files: needs its own diff-verified pass (0 rendered-field changes) + both page gates before commit. Blocks the last 6 shelves of G1 and therefore TASK-565 (run_gates in CI). Do NOT whitelist these fields in the schema.
---

# TASK-574 — Strip raw internal fields from 6 served comparison JSONs (_scoring_trace, nutrition_per_100g, duplicate name_he/image_url)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
