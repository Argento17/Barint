---
id: TASK-602
title: Full corpus traceability: re-scrape the 398 no-capture products, manifest them, verify vs published
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-11 ('do the re-scrape. full traceability of all current corpus + verification afterwards'). TASK-601 census: 398/757 served products have NO stored raw capture (bread 52, cheese 94, chocolate 58, juices 17, milk 18, yogurt-drinks 17, most yogurt-spoonable 46, partials in cakes/cookies/crackers/protein). Re-scrape each via the fixed retailer fleet (Shufersal p/p_{barcode} + fallbacks per scrape_source_selection_policy), RETAIN nutrition_raw_source, rebuild the manifest (TASK-601), re-run census to prove coverage rises toward 757/757, and REPLAY captured-vs-published to flag discrepancies. OFF BANNED absolutely. No published JSON/score changes - any discrepancy implying score movement = tripwire-1 movement table, STOP. Staged: PILOT one shelf (milk) to prove the loop, then fan out. LIVE network -> Data Agent (Codex sandbox has no network).
---

# TASK-602 — Full corpus traceability: re-scrape the 398 no-capture products, manifest them, verify vs published

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
