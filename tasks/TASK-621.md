---
id: TASK-621
title: Comma-corruption completeness: patch sibling BSIP0 nutrition paths + locale-safe disambiguation (challenge DO-NOT-SHIP)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: [TASK-614]
category_id: null
origin_task: TASK-619
lesson_trigger: recurrence
summary: >
  GPT cross-vendor challenge (verified) found TASK-619 fixed only the shared parser; 4+ sibling paths still do blind replace(',','.') BEFORE it: acquire_hazi_hinam.py:122, yohananof/parser.py:26, pipeline/extractor.py:74, salty_snacks_real/01_scrape_yoh_panels.py:56, yohananof_milk/04_parse_and_build_bsip1.py. Route them through _normalize_decimal_comma; harden 0,123 3-decimal edge case. Blocks TASK-614 re-score.
---

# TASK-621 — Comma-corruption completeness: patch sibling BSIP0 nutrition paths + locale-safe disambiguation (challenge DO-NOT-SHIP)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
