---
id: TASK-130C
title: Apply validate-corpus to launch-scope categories + remediation backlog
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "The audit achieved its objective by converting validator output into a prioritized remediation backlog with clear launch blockers and ownership"
depends_on: [TASK-130B]
blocks: [TASK-132]
category_id: null
summary: >
  Audit-only. Run validate-corpus (TASK-130B) across the launch-scope categories
  (the 5 live gen1 v2 categories: bread, hummus, maadanim, snacks, yogurts; plus
  vegetable-spreads as a hummus-derived shared corpus). Produce a readiness table,
  group ERROR/WARN findings by category+severity, recommend remediation order, and
  classify each finding as launch-blocking vs accepted technical debt. Do NOT modify datasets.
---

# TASK-130C — Apply validate-corpus to launch-scope categories + remediation backlog

Parent: TASK-130. Depends on TASK-130B (validator). Audit only — no dataset edits.
Launch scope per TASK-132 blocker: 5 live gen1 v2 categories.

## Outcome (2026-06-01) — proposed RETURNED
Report: `01_framework/operations/validate_corpus_audit_001.md`. Ran validate-corpus
(DEV + --handoff) across bread/hummus/maadanim/snacks/yogurts. No datasets modified.
Handoff-blocking errors: maadanim 96, snacks 52, bread 32, yogurts 16, hummus 3.
Three blocker classes: §2.5 unknowns backfill (142 products; hummus clean),
§2.8 NOVA framework leak (snacks, 29 occ/15 products — real, not heuristic),
§2.7 ordering (bread 6, snacks 1). Accepted debt: §2.8 health-word heuristics (R4,
QA-read), §2.4v2 advisory (R2), vegetable-spreads post-filter unvalidated (R3).
Remediation order + owner handoff in the report §4/§6. Awaiting Controller to record CLOSED.
