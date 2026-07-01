---
id: TASK-258
title: Factory: generic executable end-to-end Spine pipeline (raw to gated page)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-12
closed_at: 2026-06-12
depends_on: []
blocks: []
category_id: null
close_reason: >
  P40 delivered 03_operations/spine/pipeline_e2e.py — a generic EXECUTE-mode pipeline running
  4 real stages through the existing Spine runner. Orchestrator-verified against artifacts:
  re-ran it independently → all 4 stages SKIPPED (proves prior real execution + hash-based
  resume); spine.db has ok stage_runs for all 4 + 22 e2e lineage rows; throwaway gated page
  produced with gates G1–G6 PASS; ZERO OFF in any output; wrote only to scratch dirs
  (spine/_e2e_out, _fixtures_e2e) — no live category touched. Incremental verified (fixture
  edit re-scored 78.4/B → 80.4/A). SCOPE CORRECTION: extraction (raw HTML → BSIP1) was NOT
  wired — fixtures are already BSIP1-shaped, so the proven chain is BSIP1 → score → generate →
  gate, NOT shelf → page. That is the milestone (the DAG had never executed real stages before),
  but the front extraction stage remains the next build (TASK-259). One functional seam noted:
  score_engine.py needs a sys.path shim when run from spine/.
summary: >
  Wire the existing Spine runner + scoring (score_engine) + page-gen (generate_page) into ONE
  generic EXECUTE-mode pipeline, proven on a throwaway fixture (no live category). Closed the
  'chain never executed end-to-end' gap for BSIP1→page. Extraction (raw→BSIP1) deferred to TASK-259.
---

# TASK-258 — Factory: generic executable end-to-end Spine pipeline

**CLOSED 2026-06-12.** Deliverable: `03_operations/spine/pipeline_e2e.py` + throwaway fixtures.
Proven: the Spine DAG executes 4 real stages end-to-end (BSIP1 → score → generate → gate) with
resume, incremental, lineage, gates PASS, zero OFF. Next build: extraction Stage 0 (raw → BSIP1)
= TASK-259, which makes it a true shelf→page chain.
