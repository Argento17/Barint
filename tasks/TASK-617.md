---
id: TASK-617
title: Manifest-coverage acceptance gate: assert census delta after a scrape (catch retained-but-not-integrated)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-11
blocker: "Prevention for the TASK-615 failure class. Add a check that after captures land, build_census coverage RISES by ~the number scraped; a scrape whose captures don't register (non-canonical shape) fails the check instead of silently reporting 'files written'. Wire into the scrape/consolidation flow + a --selftest. Not yet built."
depends_on: []
blocks: []
category_id: null
origin_task: TASK-615
lesson_trigger: none
summary: >
  Structural prevention for [[scrape_capture_canonical_format]]: a manifest/census coverage-delta assertion so non-canonical captures (invisible to build_manifest) are caught at scrape time, not at a later consolidation. Acceptance = the gate FAILS on a capture written in a shape build_manifest.py can't scan, PASSES when coverage rises as expected.
---

# TASK-617 — Manifest-coverage acceptance gate: assert census delta after a scrape (catch retained-but-not-integrated)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
