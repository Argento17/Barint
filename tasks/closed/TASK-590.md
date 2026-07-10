---
id: TASK-590
title: Shelf Watch nutrition parse silently all-None: _raw-key mismatch disables nutrition_drift detection
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Escalated from TASK-582: shelf_watch.py chains bn.parse_nutrition_list() bare-keyed output into bn.parse_nutrition_numeric() which requires _raw-suffixed keys (e.g. energy -> energy_kcal_raw, exact mapping per shufersal_cereals/01_scrape_cereals.py) - every nutrition field parses to None, so the LIVE weekly monitor's nutrition_drift signal can NEVER fire (TASK-570 runs report it as quiet, not broken). Fix the key mapping in shelf_watch.py mirroring the TASK-582 fix in 01_acquire_shufersal.py, add a unit check that a known label text yields non-None fields, and re-run the canary trio. NOTE: past no_change results are untrustworthy for nutrition; ingredient_change detection was unaffected (the 2 genuine bread findings stand - they were ingredient-text based).
---

# TASK-590 — Shelf Watch nutrition parse silently all-None: _raw-key mismatch disables nutrition_drift detection

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
