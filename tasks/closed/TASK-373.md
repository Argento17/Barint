---
id: TASK-373
title: Snacks whole-food scoring relief (flagged what-if, default OFF) — intrinsic sugar/fat red-label de-anchor + SC-negation fix + date-bar routing
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-22
closed_at: 2026-06-22
work_type: go_live
red_team_cleared: true
close_reason: >
  Snacks rework shipped to bari.digital. Engine relief built behind BARI_SNACK_WHOLEFOOD_V1
  (default OFF, OFF byte-identical — C2 audit PASS). D7 co-sign: Nutrition (coconut sat-fat +
  honey loophole fixed) + Product APPROVE; C3 challenge → owner tightened to D via non-relieved
  calorie backstop. Two-gate: Content Agent authored + Adversarial QA/Red-Team PASS, 0 open
  findings (RT-M1 closed). Page render-verified HTTP 200; build exit 0 on current master
  (/hashvaot/snacks prerendered). Published as curated JSON artifact: 2 files only
  (snacks_frontend_v5.json + snacks-comparison-page-data.ts) committed c2b9d927c, pushed
  origin/master (Argento17/Barint → Vercel auto-deploy), 93f45165e..c2b9d927c. Distribution
  B1 C1 D6 E13 (snk-004/008/010=49/D, snk-009=40/D, snk-002=55/C, snk-001=66.8/B). No other
  category touched; TASK-371 D4 seed snapshot excluded. Owner approved go-live + confirmed
  deploy topology 2026-06-22.
depends_on: []
blocks: []
category_id: null
summary: >
  Flagged engine what-if (new flag default OFF, no published-score change): (1) negation-aware added-sugar so 'ללא תוספת סוכר' is not counted as added sugar (fixes SC-5 misclassification); (2) whole-food fruit/nut bar relief from binary Israeli red-label sugar+sat-fat caps where sugar/fat are intrinsic (dates, nuts, cocoa) with no added sugar/syrup/oil; (3) consistent date-bar routing lens. Deliverable: OFF-vs-ON movement table over the 21-product snacks shelf for owner review. Routed C1 build / C2 audit / C3 challenge. Tripwire-1: flip-live is owner-gated.
---

# TASK-373 — Snacks whole-food scoring relief (flagged what-if, default OFF) — intrinsic sugar/fat red-label de-anchor + SC-negation fix + date-bar routing

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
