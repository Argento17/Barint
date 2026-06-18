---
id: TASK-322
title: Bread spine conform — re-run through the uniform pipeline (freeze lifted), last zero-different category
owner: data-agent
status: CLOSED
priority: HIGH
close_reason: >
  Orchestrator-verified 2026-06-18 on branch sweep/bread-conform (HEAD 1a4b67c9, pushed).
  Bread re-run through the UNIFORM pipeline (not the bespoke lechem scorer): BSIP0 raw (258, 0 OFF) →
  BSIP1 run_bread_conform_001 (31 records) → BSIP2 run_bread_conform_001 (31 scored, standard traces) →
  generate_page configs/bread.json → 29 displayed / 2 G8-discarded. VERIFIED: all 8 gates PASS, G4 OFF=0,
  flags EXACTLY match the cereals grain analog (RECAL_P0=on, SHELF_RELATIVE=off, FAT_TECH=on — not an
  artifact). Grades honest (S2/A11/B14/C2 on the curated-best scope that was already live; top לחם טחינה
  94.8/S rides on real 27.5g protein/18.5g fiber, spot-checked). Copy pass (Content Agent, Sonnet): all
  29 rowVerdicts + 26 insightLines authored from real traces to gold-standard bar, 0 PENDING remaining,
  Hebrew-leakage scan clean. Final build exit 0, 39 pages, /hashvaot/bread present. Scores moved vs the old
  lechem numbers — expected + owner-accepted ("uniformity only"). Shell copy stays in bread-comparison-page-data.ts.
  Merge to master = owner go-live gate (PR pending). Bread is the LAST structurally-different category →
  after merge, every live /hashvaot category is on the uniform spine.
created_at: 2026-06-18
depends_on: [TASK-321]
blocks: []
category_id: bread
summary: >
  Owner lifted the bread provenance freeze 2026-06-18 ("do like you did for milk") so bread can join the
  uniform spine. Unlike milk (standard traces already existed → config drop-in), bread's live scores came
  from a BESPOKE "lechem" scorer (calibrate_lechem_scores.py / build_lechem_frontend_json.py) — there are NO
  standard BSIP2 traces and no bsip1 records. So conform = re-run the existing OFF-clean BSIP0 raw
  (real_bread_retail_003_v1, 258 products, 0 OFF refs) through BSIP1 → BSIP2 (uniform engine) → generate_page
  with a new configs/bread.json, then repoint the (already-uniform) bread frontend loader. Scores WILL move
  (uniform engine vs lechem calibration); owner accepts ("uniformity only, scores don't matter"). Last
  structurally-different category — after this, every live /hashvaot category is on the uniform spine path.
---

# TASK-322 — Bread spine conform (freeze lifted)

## Owner authorization (2026-06-18)
Owner lifted the bread provenance freeze ("yes do like you did for milk"). This supersedes the CLAUDE.md
frozen-invariant ruling for bread provenance/curation. Score movement is accepted.

## Why bread is different from milk/cheese/yogurt
- Milk/cheese/yogurt: real BSIP2 engine traces already existed → conform was a config drop-in + frontend wiring.
- Bread: scored by a SEPARATE bespoke "lechem" pipeline. `02_products/bread_retail_003/bsip2/bsip2_shufersal_*.json`
  are a custom schema (final_score/final_grade), NOT standard bsip2_trace.json. No bsip1 records exist.
  generate_page cannot read them. → bread must be RE-SCORED through the uniform engine from the BSIP0 raw.

## Inputs (verified)
- BSIP0 raw: `02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json` — 258 products, **0 OFF refs**.
- Curated scope: `..._curated_comparison_dataset.json` — 31 curated products (live page shows 19 / 24 scored from this).
- Live copy source: `bari-web/src/data/comparisons/bread_frontend_v2.json` (19 products, owner-signed copy to carry).
- Config templates: `configs/{yogurts,cheese,milk}.json`. Generator: `generate_page.py --config … --out …` (self-gates).
- Bread products key on Shufersal product_id (NO barcodes) — pipeline must preserve canonical_product_id keying.
- No bread code-gate in rescore_all.py (freeze was doc-only; nothing to retire).

## Dispatch: Data Agent (2026-06-18), worktree C:\bari-breadconform → branch sweep/bread-conform
End-to-end pipeline re-run + config + generate (gates PASS, OFF=0) + frontend repoint + build + push.
RETURNED-UNVERIFIED until orchestrator verifies (gate table, OFF=0, build exit, grep-clean) — mirrors milk verification.
