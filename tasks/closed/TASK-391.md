---
id: TASK-391
title: Chocolate-tablets rework (freshness re-score + de-recite copy + metric + intro)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-24
closed_at: 2026-06-24
depends_on: []
blocks: []
category_id: null
close_reason: >
  Shipped + live-verified at bari.digital/hashvaot/chocolate-tablets (commit c294039e3,
  18377e62d..c294039e3 on master). Live poll confirmed: new de-recited intro present,
  old gram-recitation intro gone, ct-004 absent (38->35 discard live).
  VERIFIED against artifacts:
  - Freshness re-score = scores current (0 grade movers).
  - Discarded ct-004/005/006 (C50 milk-chocolate scored on MISSING ingredient data,
    per missing-data discard rule) -> 38->35, C9/D9/E20 -> C6/D9/E20.
  - All 35 verdicts de-recited insight-first (sugar shows as a bar + Bari score; cocoa %
    is the kept differentiator). 0 residual gram/kcal/mg recitations (incl. ct-001/ct-036
    re-cleaned after the fix pass re-introduced two).
  - Two-gate signed off: Adversarial QA + C3 (P393) -> caught/fixed a false
    "most-engineered" superlative (ct-016) + grammar + 11 mediums.
  - Naturalness gate 0 HIGH (excl. accepted site boilerplate).
  - Deploy delta = exactly 2 files (JSON + page-data.ts); diff against live caught a
    featured-card regression (local had reverted theme img to snacks.jpg; live already
    correct) and it was excluded. Build passed clean; chocolate-bars + magnesium track
    untouched.
  Open follow-up (NOT a blocker): ME-7 -- chocolate scoring trace tags category as
  "snack_bar_granola"; scores confirmed current, but the category-lens choice deserves a
  later methodology review.
summary: >
  Parallel shelf alongside juices TASK-389. Live chocolate_tablets_frontend_v1.json (Jun 21, 38 products, healthy C9/D9/E20 spread, 38/38 verdicts recite panel). Recent build so scores likely current. Stages: freshness confirm -> de-recite all 38 + sugar metric -> intro -> two-gate -> deploy.
---

# TASK-391 — Chocolate-tablets rework (freshness re-score + de-recite copy + metric + intro)

CLOSED 2026-06-24 — see close_reason. Live at bari.digital/hashvaot/chocolate-tablets.
