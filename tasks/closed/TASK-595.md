---
id: TASK-595
title: Corpus-wide damage scan: ALL published nutrition fields vs in-repo raw panels (extends TASK-591)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner directive 2026-07-11 ('let's see what the damage is - scan for other shelves'). TASK-591 scanned one signature (fat==0.5, EV-026): 15/20 cereals CONFIRMED wrong. Extend to the full question: for EVERY product in EVERY served *_frontend_v*.json, replay every persisted in-repo raw panel (nutrition_raw_source.rows under 02_products/** and 03_operations/bsip0/**) through the correct *_raw mapping and diff EVERY nutrition field against the published expansion.nutrition values. Bucket deltas by magnitude (rounding-level vs material) so damage is measured honestly. READ-ONLY; no corrections; any score-movement implication = tripwire-1 movement table only. BUILD-LIGHT Codex terra, worktree.
---

# TASK-595 — Corpus-wide damage scan: ALL published nutrition fields vs in-repo raw panels (extends TASK-591)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
