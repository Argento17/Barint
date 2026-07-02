---
id: TASK-358
title: Clear baseline: canonical shelf-data contract + conformance checker + drift report
owner: frontend-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
summary: >
  Owner wants ONE enforced data baseline so shelves stop drifting. Define the canonical per-product field contract from the golden cereals/juices shape (deep-dive layer OUT, curation rules baked in: drop no-image, dedupe size-variants, re-derive rank; brand deferred). Build conform_baseline.py checker (exit 0/nonzero) + a drift report for all 10 shelves. NO data mutation in this task — design+measure only. Then a conform sweep follows.
---

# TASK-358 — Clear baseline: canonical shelf-data contract + conformance checker + drift report

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
