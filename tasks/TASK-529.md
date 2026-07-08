---
id: TASK-529
title: 7290119377411 (spoonable yogurt): expansion.ingredients text names E1442+locust-bean-gum but scored d4_additives shows E1422+E330 (citric acid) -- separate from the RT-2H1 tapioca-fix product set
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced during TASK-504A GATE-2 re-gate (QA independently cross-checked this product's data while verifying the RT-1 additive-naming fix). The product's displayed ingredient text says 'עמילן טפיוקה מעובד (E1442)' + 'מייצב (לוקוסט-בין גאם)' but its scored d4_additives card shows E1422 (different E-number, modified starch) + E330 (citric acid, contested tier) -- a real internal inconsistency between displayed label text and the scored additive card. This barcode was NOT one of the 16 products in this session's RT-2H1 tapioca-starch classifier fix -- unrelated drift, needs its own investigation (same failure shape as RT-C4 earlier this session -- E-number/label mismatch -- but a different product and possibly a different root cause).
---

# TASK-529 — 7290119377411 (spoonable yogurt): expansion.ingredients text names E1442+locust-bean-gum but scored d4_additives shows E1422+E330 (citric acid) -- separate from the RT-2H1 tapioca-fix product set

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
