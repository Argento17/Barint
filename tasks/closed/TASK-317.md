---
id: TASK-317
title: Spine step 2 — affected-set from a flag (wrap Shadow diff --set → which categories moved → which shelves to re-run)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-316]
blocks: [TASK-319]
category_id: null
close_reason: >
  C1-GROK built 03_operations/page_generator/affected_set.py. Orchestrator-verified independently: manifest schema correct
  (flag_overrides/shadow_verdict/shadow_exit_code/frozen_touched/affected/affected_shelves/frozen_breaches/affected_no_config);
  on the frozen sample report → frozen_touched=true, frozen_breaches=[milk,snack_bars], affected_shelves correctly mapped
  (cereals/granola/hard_cheeses/hummus_shelfrel_002/snacks), unmapped moved corpora (cheese/maadanim/milk/yogurt) flagged under
  affected_no_config not dropped, exit 2. Exit-code matrix verified (2 frozen / 1 movement / 0 clean) + a real --set what-if
  (BARI_GLASSBOX_W4=on) resolved end-to-end in 3.1s → shelves cereals+hummus, exit 1. Read-only over shadow/registry/configs;
  no engine/page edits. Feeds step-4 orchestration.
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
