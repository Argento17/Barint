---
id: TASK-573
title: US shelf comparison capability: expose USDA FDC Branded ingredient text
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner asked (2026-07-10, TASK-557) what US shelves look like vs Israeli shelves for sweeteners. Feasible but not built. USDA FDC Branded foods carry ingredient text + gtin_upc, and usda_fdc is an approved LIVE-VERIFIED source (OFF remains banned). Gap: integrations/clients/usda_fdc.py Food dataclass does not expose the 'ingredients' field, and search() needs data_type=['Branded']. Needs FDC_API_KEY (DEMO_KEY is rate-limited; no paid service). Scope: extend the client to return ingredients for Branded foods, then run the same sweetener token scan used on the Israeli corpus to produce an honest cross-market comparison. Cross-market output is ANNOTATE-ONLY and must never move a score (cross_market_disclosure_concept). Consumer-facing use would need the two-gate.
---

# TASK-573 — US shelf comparison capability: expose USDA FDC Branded ingredient text

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
