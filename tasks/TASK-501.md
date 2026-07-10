---
id: TASK-501
title: Cookies comparison page: reconcile 117 vs 119 product-count discrepancy in page_copy (live)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-04
blocker: "Red-team RT-3 finding (TASK-492A gate). Not yet dispatched: cookies_coffee_frontend_v2.json has an uncommitted unrelated main-tree change; needs base=origin/master worktree + own two-gate + owner merge. Surface to owner before dispatch."
depends_on: []
blocks: []
category_id: null
summary: >
  cookies_coffee_frontend_v2.json: product array/_meta say 117 products (E:81) but page_copy hero/caveat/filters say 119 (E:83) — live /hashvaot/cookies-coffee likely renders stale 119/83. Blog's 117 is verified correct. Also RT-4: ck-7290109354996 trace final_score_estimate 10.7 vs displayed 10.0 (grade unaffected). Score-neutral data-hygiene fix; no scoring change.
---

# TASK-501 — Cookies comparison page: reconcile 117 vs 119 product-count discrepancy in page_copy (live)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
