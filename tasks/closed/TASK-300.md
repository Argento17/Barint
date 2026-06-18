---
id: TASK-300
title: Data remediation — root-cause + fix corrupt BSIP1 source data exposed by re-baseline (granola sodium 6k-10k mg ×5, hummus 7296073705505 nutrition-panel-as-ingredients)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Data Agent (2 rounds) + orchestrator-verified. ROUND 1: root-caused granola sodium = parse_sodium_mg <=10-no-unit x1000 on
  OLD 2026-06-01 scrapes; fixed 9 sodium records (parser left as-is, correct for new unit-bearing scrapes; G8 backstops). ROUND 2
  (after orchestrator found round-1 sweep incomplete via G8): proper gate-logic sweep of 722 records/10 corpora found 8 unique
  panel-as-ingredients barcodes (2 hummus + 6 cereal/granola), 13 file instances fixed; post-fix G8 sweep = 0 hits. ORCHESTRATOR
  re-ran trigger + verified: G8 PASS all 9, C10 milk Δ0 all 9, OFF=0, score==trace ok, snacks max 70/B. RT-2 (granola sodium) +
  RT-3 (hummus garbage ingredient) RESOLVED at data level. Ingredient corrections shifted some cereals/granola scores (more
  correct). Scope: BSIP1 source JSONs only (engine/config/bari-web/run_gates untouched by data scripts). Stray sweep scripts cleaned.
  Residual (non-blocking): 3 raw-chickpea products mis-shelved on hummus = Product curation; fat_g=0.5 EV-029 overwrite on 9 granola
  needs re-scrape (flagged, out of scope).
depends_on: [TASK-299]
blocks: []
category_id: null
summary: >
  Root-cause + fix the corrupt source data the re-baseline exposed: (1) 5 granola products with impossible sodium 6000-10000mg/100g (real granola ~30-100mg) — find the BSIP0 parse/unit bug, fix the parser if systematic, re-derive correct sodium from raw scrape, sweep all shelves for the same defect; (2) hummus 7296073705505 ingredient field = scraped nutrition-panel text (4 load_errors) — re-derive real ingredients from scrape or NULL it (never fabricate; OFF-ban). No score is correct until source data is. Verify against raw_store scrape.
---

# TASK-300 — Data remediation — root-cause + fix corrupt BSIP1 source data exposed by re-baseline (granola sodium 6k-10k mg ×5, hummus 7296073705505 nutrition-panel-as-ingredients)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
