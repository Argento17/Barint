---
id: TASK-259
title: Factory: wire extraction Stage 0 (raw HTML to BSIP1) into pipeline_e2e
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-12
returned_at: 2026-06-12
closed_at: 2026-06-12
depends_on: [TASK-258]
blocks: []
category_id: null
close_reason: >
  P41 wired extract_bsip0 + build_bsip1 as Stage 0/0.5; the chain now starts at raw HTML.
  Orchestrator-verified against artifacts: independent re-run → all 5 stages SKIPPED (proves
  real execution + hash-resume); spine.db stage_runs ok for extract_bsip0/build_bsip1/
  score_products/generate_page/gate_page; old BSIP1 fixtures deleted (no fixture_ingest
  shortcut — chain genuinely starts at raw); ZERO OFF markers across all BSIP0+BSIP1 outputs
  with a runtime _off_data_used:false guard; raw→score trace real (HTML value="14" protein →
  BSIP1 protein_g 14.0 → grade A); gates G1–G6 PASS; throwaway scratch dirs only, no live
  category touched. The factory now executes a true shelf→page chain on synthetic fixtures.
  Remaining: page is structurally gated but copy is PENDING_COPY (copy stage not yet in the
  DAG); trust layer (dual-extractor + invariants) not built; not yet run on real retailer HTML.
summary: >
  Add real extraction front-stage to pipeline_e2e.py: raw HTML -> BSIP0 (replay_parse) -> BSIP1, feeding the proven BSIP1->score->generate->gate chain. Makes it a true shelf->page execution. Throwaway fixture only; OFF-ban enforced on extraction.
---

# TASK-259 — Factory: wire extraction Stage 0 (raw HTML to BSIP1) into pipeline_e2e

## Deliverable (RETURNED 2026-06-12)

Stage 0 (extract_bsip0) and Stage 0.5 (build_bsip1) added to pipeline_e2e.py.
Chain is now: raw HTML → extract_bsip0 → build_bsip1 → score_products → generate_page → gate_page.
Old BSIP1 fixture files removed. Chain genuinely starts at raw HTML.
All 5 stages pass. All 6 page gates pass. OFF ban confirmed zero. Resume + incremental hold.

See return contract below.
