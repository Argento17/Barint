---
id: TASK-465
title: Catalog redesign: sharp data-dashboard look (PowerBI-grade) for /catalog
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-02
closed_at: 2026-07-02
close_reason: >
  Merged via PR #47 (merge d8d95c16), both Vercel deploys success, production-verified 8/8 with
  cache-bust: KPI strip live, full-data KPI shows the corrected truthful 67% (52% gone), distribution
  bar, sticky markup + overflow-clip fix served. Build chain: Cursor P472 (commit 251021ef, KPIs
  live-derived, contract + screenshots) + orchestrator completion on explicit owner mandate
  (d2554114: sticky un-trapped + DOM-verified pinned @68px, confidence "full"→"verified" loader
  normalization per VM contract fixing QA H1/H2, L1/L2 suppressions, orphan cleanup). Two-gate:
  Content GO 8/8 labels; Adversarial QA (Opus) GO_WITH_FIXES with independent 9/9 KPI recount, both
  HIGHs resolved + re-gated (tsc/lint/build 0). Follow-ups routed: cheese "full"-confidence source
  normalization (data-agent), mobile numeric-score polish (M2).
depends_on: []
blocks: []
category_id: null
summary: >
  Owner directive 2026-07-02: current /catalog looks cheap; redesign to a sharp, data-dense dashboard aesthetic (PowerBI-grade): KPI header strip, professional data-grid, grade distribution visuals, refined filter/slicer bar, tight numeric alignment, muted professional palette on existing site tokens, RTL Hebrew. No data changes, no consumer-claim changes; new micro-labels go through two-gate before owner PR. Catalog is NOT under the frozen comparison-page system but must stay token-coherent with the site.
---

# TASK-465 — Catalog redesign: sharp data-dashboard look (PowerBI-grade) for /catalog

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
