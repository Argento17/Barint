---
status: CLOSED
priority: medium
owner: content-agent
created: 2026-06-10
updated: 2026-06-10
closed: 2026-06-10
category: editorial
roadmap_impact: false
tags: [copy, hebrew, framework-invisibility, yogurt, governance]
supersedes: []
superseded_by: []
ancestry: "TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 (closed) — D3b unsafe-wording gate caught CMP-06:NOVA"
close_reason: >
  Removed literal "NOVA 3"/"NOVA 4" from 3 yogurt products' consumer copy in
  yogurts_frontend_v3.json — 6 strings total (3 insightLine + 3 rowVerdict; rowVerdict
  carried the identical leak, fixed for completeness). Gram values preserved exactly;
  nothing invented (nutrition-agent verified). NOVA tag carried zero consumer meaning,
  so consumer meaning is preserved. Acknowledged_exception CMP-06:NOVA REMOVED and the
  pairwise unsafe-wording gate now passes on the fixed copy WITHOUT any exception;
  run_d3_ci.py ALL 7 GATES GREEN. No scoring/data/frontend-code changes.
  OUT-OF-SCOPE findings surfaced for follow-up (NOT fixed here): (1) salty_snacks
  build_insight_line emits "NOVA N — עיבוד גבוה" into insightLine+rowVerdict for 28
  products (deterministic builder — needs a builder change + golden_diff re-snapshot
  under the D4 protocol); (2) olive_oil expansion copy has 11 NOVA mentions;
  (3) gate-coverage gap — the unsafe-wording scan covers insightLine+expansion but NOT
  rowVerdict, and deterministic insightLines aren't wording-scanned at all. Recommend
  one follow-up task to fix (1)+(2) then extend gate coverage (3).
---

# TASK-BARI-COPY-LEAK-YOGURT-NOVA-V1: Remove literal NOVA 3/4 leak from yogurt copy

## Objective
Rewrite the affected yogurt `insightLine`s to remove literal `NOVA 3` / `NOVA 4`
framework terminology while preserving consumer meaning.

## Scope
- Yogurt `insightLine`s only.
- Remove framework terms: `NOVA`, `NOVA 3`, `NOVA 4`, ultra-processing class labels.
- Keep copy short, Hebrew, consumer-facing. No health claims. No scoring/data/frontend
  behavior changes beyond updating the authored copy source.

## DoD
1. [x] Every yogurt insightLine containing NOVA terminology identified (3 products;
       also found in their rowVerdict — same leak, fixed too).
2. [x] Rewritten into Bari consumer language (framework-invisible) — trailing
       "— NOVA N" dropped; protein/fat facts retained.
3. [x] nutrition-agent verifies factual accuracy — all gram values preserved exactly.
4. [x] qa-agent reran unsafe-wording gate; CMP-06:NOVA clears WITHOUT the
       acknowledged_exception (exception removed; gate green on fixed copy).
5. [x] No other prompt-governance gate regresses — run_d3_ci.py 7/7 GREEN.

## Out-of-scope findings (NOT fixed — recommend follow-up)
- salty_snacks `build_insight_line` NOVA branch leaks into 28 products' insightLine+rowVerdict (deterministic builder; needs builder change + golden_diff re-snapshot).
- olive_oil expansion copy: 11 NOVA mentions.
- Gate-coverage gap: unsafe-wording scan misses rowVerdict and deterministic insightLines.
