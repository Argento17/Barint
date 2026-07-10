---
id: TASK-466
title: Derived live_manifest: one generated source of truth for live categories; conformance + CI drift check
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-02
closed_at: 2026-07-02
close_reason: >
  Merged via PR #46 (merge da637dca); master CI run SUCCESS including the new live_manifest --check
  step on Linux. P473 (registry-derived, 7 categories) was CHANGES_REQUESTED by the orchestrator —
  it re-encoded the registry blind spot and would have shrunk conformance 18→7; P474 rework derives
  from app routes: 22 routes / 16 comparison categories (9 bespoke routes the registry missed, all
  covered), 0 gaps, conformance --all = 16 manifest stems (old 18 minus 2 proven staging/discard
  configs), 14/16 conform (bread+cheese HARD-3 pre-existing). Orchestrator re-ran --check (PASS) and
  independently recounted routes. Follow-ups routed: rescore_all/spine_flip manifest adoption (scoped
  in contract); router-regression exit-code liveness defect + dairy_flavor_contamination_biscuit
  corpus FAIL → TASK-453 backlog / nutrition.
depends_on: []
blocks: []
category_id: null
summary: >
  P0-4 launch-report item (owner approved). Tooling carries hand-maintained live-category lists that go silently stale (6 categories found outside the safety net; enabled TASK-463 class). Build live_manifest.py deriving manifest from the frontend comparisons registry + page-data imports; --check drift mode; conformance.py --all reads manifest; CI step added. rescore_all/spine_flip adoption scoped as follow-up.
---

# TASK-466 — Derived live_manifest: one generated source of truth for live categories; conformance + CI drift check

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
