---
id: TASK-617
title: Manifest-coverage acceptance gate: assert census delta after a scrape (catch retained-but-not-integrated)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
close_reason: >
  Prevention gate DELIVERED (data-agent, commit e19d14fa) + orchestrator-verified. coverage_gate.py
  (+ known_not_found_allowlist.json, 17 sourced entries): --files mode detects a capture whose data is
  present but shape is invisible to build_manifest (the exact TASK-615 class) and FAILs naming the
  file+GTINs; --corpus mode FAILs on any served product missing a canonical capture not on the
  allowlist. VERIFIED: commit=2 files, --selftest PASS (fails on synthetic non-canonical, passes on
  canonical), allowlist=17. Agent also ran a REAL e2e (dropped a non-canonical file into the scan root
  → --files exit 1, then restored manifest to zero-drift). --corpus current = 693/710, 17 allowlisted,
  0 unexplained → PASS. Honest spec-conflict flagged (17 real vs my ~15 estimate — each traced to a
  source). Closes the TASK-615 lesson loop (615 lesson_outcome=implementation_task → this task).
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
