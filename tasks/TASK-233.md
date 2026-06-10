---
id: TASK-233
title: "Project Glassier — end-to-end audit of the BSIP0 → Comparison Page pipeline (process, agents, engine, weaknesses)"
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: []
blocks: []
roadmap_impact: true
work_type: audit
---

# TASK-233 — Project Glassier: full-pipeline audit

Owner directive (2026-06-10): "Audit carefully the whole BSIP0 → Comparison Page upload
(final, after content + frontend polish). Articulate the whole process. Divide into
STEP1, STEP2, STEP3… and for each STEP define: agents responsible, how the engine runs it,
weaknesses + a suggestion to fix/improve. High demand, high priority, extremely important."

## Scope
The complete path a category travels from raw shelf data to a live, polished comparison page:
BSIP0 extraction → scope → BSIP1 enrichment → routing → BSIP2 scoring → QA → Red-Team →
content → frontend JSON packaging → D4 wiring → frontend integration → design polish →
pre-launch QA → upload/go-live.

Each STEP documents: (1) what happens / how the engine runs it (concrete scripts + files),
(2) the agent(s) responsible, (3) weaknesses, (4) a concrete fix/improvement.

## Grounding (no invention)
Audit is grounded in the actual frozen-vegetables run (`run_frozen_vegetables_001`) and the
real code: `bsip0_nutrition.py`, `ingredient_enricher.py`, `router_v2.py`, `score_engine.py`,
the per-category `generate_frozen_vegetables_frontend.py`, `corpus.ts`, the shelf-filter +
page-data modules, the view model, and the `bari-category-factory` / `bari-qa-audit` skills.

## Output
`01_framework/operations/project_glassier_pipeline_audit_v1.md` — the articulated STEP-by-STEP
audit + a prioritized weakness register (CRITICAL / HIGH / MEDIUM) with owning agents.

## Acceptance criteria
- [x] Every STEP from BSIP0 to go-live articulated with the four required facets
- [x] Each weakness names the real file/behavior it stems from (no generic findings)
- [x] Each weakness carries a concrete, owner-assigned fix
- [x] Prioritized register at the end; severity grading is conservative (verified, not assumed)
- [x] No scores, engine, or published JSON changed — audit only

## Confirmation sweep (2026-06-10)
Read-only cross-category sweep dispatched to data-agent ‖ qa-agent (reviewers: content,
frontend). Result: `reports/task_233_confirmation_sweep.md`.
- All 3 root causes CONFIRMED SYSTEMIC (no shared packaging core ≥10 generators; late/manual
  validation — no build gates; editorial copy escapes — grade literals in 4 live categories).
- New findings beyond the original audit: grade computed twice → real drift on ≥9 products
  (DA-009); generator/runtime field-name mismatches (DA-010/011).
- Verdict: **PASS WITH FIXES.** Recommended subtasks: 233A validation-gate harness · 233B shared
  packaging core (+confidence) · 233C editorial copy routing+policy · 233D targeted data fixes.
- Holds: frozen_vegetables go-live held (DA-005/006 confidence inflation — "full data" while
  listing gaps; still pre-merge on preview branch). cereals rescore-narration leak (QA-003)
  fast-tracked. No emergency pause of live snacks/cereals/bread (grade-literal = Content/Design
  policy ruling pending, pre-existing style).

Status stays IN_PROGRESS pending the owner's decision on opening 233A–233D.
