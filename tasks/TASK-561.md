---
id: TASK-561
title: Bread live-route cutover decision: re-point bread config baseline_json v3 -> v4 (or re-derive)
owner: product-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced by TASK-560 conformance work. bread.json baseline_json still targets bread_frontend_v3.json while live_manifest + bari-web (bread-comparison-page-data.ts, admin/fields.ts) serve bread_frontend_v4.json. Config comment (2026-07-01, TASK-433) states this is DELIBERATE: v4 was a membership-correction-only build (crackers split out, 23 survivors, byte-identical scores) produced OUTSIDE this config, and a full re-score through the config drifts one survivor -0.8pts due to a post-v3 router rule -- re-scoring was explicitly REJECTED. The cutover is called a go-live/wiring decision for Frontend/Product, out of Data Agent lane. CONSEQUENCE: a spine_flip today re-flows into orphaned v3 while the site serves v4 -> bread silently goes stale. This is the sole standing conformance non-conformer (HARD-3-baseline_served). Decide: (a) re-point baseline_json to v4 and accept/handle the -0.8 drift on next re-score, (b) re-derive v4 through the config properly, or (c) formally accept v3-as-score-of-record and document the flip behavior. Do NOT silently re-point.
---

# TASK-561 — Bread live-route cutover decision: re-point bread config baseline_json v3 -> v4 (or re-derive)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
