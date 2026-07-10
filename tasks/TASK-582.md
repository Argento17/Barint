---
id: TASK-582
title: BSIP0 Shufersal acquisition script 404s on every request (stale URL template)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found during TASK-570: 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py 404s on all requests - stale URL template. The verified-live path is .../online/he/p/p_{barcode} (Shelf Watch uses it successfully). Fix the acquire script and canary-test it; the BSIP0 retailer-fleet READY claim is stale for Shufersal until then.
---

# TASK-582 — BSIP0 Shufersal acquisition script 404s on every request (stale URL template)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
