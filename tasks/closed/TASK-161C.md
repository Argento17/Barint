---
id: TASK-161C
title: Wire rowReason + metricSpecs into all 6 comparison page-data/page files
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — verified + QA-confirmed (TASK-161D). All 6 pages wired: cheese/yogurts metricSpecs=DAIRY_PROTEIN_METRIC (scaleMax 8, resolves the low-bar flatness), vegetable-spreads/bread=PROTEIN_METRIC, snacks=[] (no bar, all nutrition null), milk=MILK_METRIC_SPECS unchanged. rowReason wired via new shared src/lib/comparisons/row-surface.ts (enrichRowSurface / enrichRowReasonOnly — verbatim mirror of hummus's helper, prevents drift). Display-only: bread/snacks JSON byte-identical to HEAD; score/grade are pass-through VM fields. tsc/build(34 routes)/lint/corpus-validate all exit 0. One follow-up flagged (not blocking): vegetable-spreads uses per-100g PROTEIN_METRIC not the per-100ml dairy preset (aria-unit correctness)."
depends_on: [TASK-161A, TASK-161B]
blocks: []
category_id: null
summary: >
  Copy the hummus pattern (rowReason from positiveSignals[0]/limitingFactors[0] via shortenReason + metricSpecs) into cheese/bread/yogurts/snacks/vegetable-spreads/milk page-data + page files. Mechanical once data exists. tsc+build+corpus-validate clean.
---

# TASK-161C — Wire rowReason + metricSpecs into all 6 comparison page-data/page files

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
