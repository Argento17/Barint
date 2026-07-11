---
id: TASK-614
title: Corrected-nutrition re-score: bread fat placeholder (+ other MATERIAL shelves) — orchestrator authority |Δ|≤30
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-07-11
blocker: "Sequenced AFTER (a) TASK-602 re-scrape baseline complete (batch-5 pending) + consolidated manifest rebuild, and (b) BSIP0 parser fix lands (other session). NOT owner-gated: score movements are the orchestrator's authority (owner ruling 2026-07-11, |Δ|≤30; bread diagnosed max |Δ|=6, 1 grade flip B->C on keto bread 7290014321168). Re-score bread on the CURRENT engine with corrected nutrition via the uniform pipeline (re-enrich BSIP1 from batch-3 captures -> BSIP2 -> generate), full re-audit + Adversarial QA gate, verify every |Δ|<=30 (>30 = defect, stop). Fold in other MATERIAL shelves the re-scrape surfaced (cheese 3, +batch-5). EXCLUDE 7290016967074 (name/SKU identity anomaly, route to Data Agent separately). Consumer deploy still owner-merge."
depends_on: []
blocks: []
category_id: null
origin_task: TASK-612
lesson_trigger: none
summary: >
  Bread bsip2 traces scored on placeholder fat (0.25/0.5g) not real (1-9.1g) — VERIFIED (trace L1 fat_g=0.25 + fat_quality formula reproduced 18/18). Correcting lowers 14/18 by 0.1-6.0pts, flips 1 grade B->C. Systematic re-score on current engine (fixes TASK-563 non-derivability for bread as bonus). Evidence: bread_diff.json + scratchpad task612 sim.
---

# TASK-614 — Corrected-nutrition re-score: bread fat placeholder (+ other MATERIAL shelves) — orchestrator authority |Δ|≤30

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
