---
id: TASK-317
title: Spine step 2 — affected-set from a flag (wrap Shadow diff --set → which categories moved → which shelves to re-run)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-316]
blocks: [TASK-319]
category_id: null
summary: >
  Build the affected-set resolver: given a scoring flag what-if (BARI_X=on), produce the clean list of categories that move +
  the rescore_all shelves to re-run. Shadow already does the heavy lifting — `shadow_backtest.py diff --set FLAG=VAL` writes a
  structured shadow_report.json (per-corpus class/n/moved/grade_changes/added_pids/removed_pids/invariant_violations/moves +
  verdict/exit_code). Step 2 = a thin resolver that runs (or reads) that report, marks each corpus affected if it moved
  (moved>0 OR grade_changes OR added/removed pids OR invariant_violations), maps corpus name → config/shelf key, flags
  frozen-touched as a BLOCK (mirror shadow exit 2), and emits affected_set.json + a human summary. Read-only over shadow /
  registry / configs; NO engine/scoring/page edits. This feeds step 4's orchestration. Route C1-GROK (spec-complete).
---

# TASK-317 — Spine step 2: affected-set from a flag

See `tasks/prompts/P167_affected_set.md`. Consumes Shadow's report; feeds the step-4 orchestration.
