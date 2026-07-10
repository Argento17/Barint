---
id: TASK-570
title: Shelf Watch pilot: weekly label-change monitor for cereals + bread (alert-only)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10, pilot scope only. Weekly lightweight re-scrape (nutrition + ingredients) of live cereals + bread corpora via the existing retailer engines; diff vs last BSIP0 snapshot; classify cosmetic/nutrition_drift/ingredient_change/page_gone; surface in owner digest. ALERT-ONLY: never changes scores, never auto-publishes; failed scrape = discard per missing-data rule, never a drift signal. Must run as a LOCAL scheduled task (cloud lanes cannot push - Hebrew Health Scan precedent). Design doc + canary adapter-health check first.
---

# TASK-570 — Shelf Watch pilot: weekly label-change monitor for cereals + bread (alert-only)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
