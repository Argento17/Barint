---
id: TASK-330
title: Generator render-contract gap: emit comparisonContext + fix banned-phrase copy (spine PASS prerequisite)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-18
depends_on: []
blocks: [TASK-331]
category_id: null
close_reason: >
  Chartered render-contract scope DONE + orchestrator-verified. (1) G1 SCHEMA: comparisonContext now derived on
  copy_stage carry-forward via existing author_copy._comparison_context (P216, copy_stage.py +72) → FAIL→PASS both
  shelves (cereals 20/20, hummus 57/57). (2) G6 COPY-SAFETY: all 9 violations cleared → PASS both shelves —
  Content Agent fixed 4 hummus (חלבון נמוך + sodium-causal) + 5 sodium-causal (3 cereals/2 hummus) in source copy;
  C1-CURSOR fixed 1 genuine grade-letter error (7290107647854 ג→ד); C1-GROK applied the C3-reviewed gate
  word-boundary fix (run_gates.py SODIUM_CAUSAL_PATTERN — kills the כי-in-נמוכים / בשל-in-מבשל EV-051-class
  false-positive project-wide). Final clean-tree spine run = 7/8 gates PASS, score_moves=0, frozen breach none.
  P219 scope violation (Grok rogue-edited spine_flip.py/affected_set.py/shadow_backtest.py) caught + reverted to
  HEAD; regex independently re-verified (regression 8/8). REMAINING G2 COVERAGE (3 SKUs missing sugar) is a
  pre-existing data gap, OUT of render-contract scope, must NOT be fabricated (missing-data rule) → spun to
  TASK-331 (owner ruling 2026-06-18: allow documented nulls in G2, Nutrition-owned). affected_set over-inclusion
  logged for future spine-tooling refinement.
summary: >
  Spine first-run (TASK-327) proved every flip returns gates REVIEW (never PASS) because generate_page/render_fields does NOT emit comparisonContext (G1 schema FAIL) and cereals/hummus carry banned-phrase copy (חלבון נמוך, sodium causal framing → G6). Port comparisonContext derivation into the generator + remediate the copy so a clean flip can reach PASS. THE #1 'flip-a-switch' unlock. Also: affected_set over-includes 0-move shelves (can't separate flag-delta from baseline drift) — log for spine-tooling refinement.
---

# TASK-330 — Generator render-contract gap: emit comparisonContext + fix banned-phrase copy (spine PASS prerequisite)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
