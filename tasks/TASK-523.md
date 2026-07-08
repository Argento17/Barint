---
id: TASK-523
title: Live 3-category re-flow: modified-tapioca-starch classifier fix (hummus/cakes/crackers, 28 products, up to 4 grade crossings)
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-07-08
blocker: "owner approval required — consumer-facing deploy, tripwire 2"
depends_on: []
blocks: []
category_id: null
summary: >
  Classifier bug (ingredient_taxonomy.py) fixed + co-signed (Nutrition+Product+C3) during TASK-515/515A. Applied ONLY to pre-launch yogurt so far. Live categories hummus(3)/cakes_hard_cookies(8)/crackers(1) = 12 products flip native->modified_starch, 4 cross a grade boundary, all downward/more-accurate. Regen+redeploy needs explicit owner go-ahead. See TAPIOCA_STARCH_FIX_COSIGN.md + red_team_yogurt_drinkable/spoonable_task515*_v3.md for full provenance.
---

# TASK-523 — Live 3-category re-flow: modified-tapioca-starch classifier fix (hummus/cakes/crackers, 28 products, up to 4 grade crossings)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
