---
id: TASK-168J
title: Surface saturated fat in the cheese + yogurt nutrition table (owner-approved display add)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
cc_reviewed: 2026-06-03
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
close_reason: "Owner-approved sat-fat display add SHIPPED + gate-verified. Data added nutrition.satFat (grams, verbatim from L1_observed_signals.fat_saturated_g in run_cheese_004 / run_yogurt_004 traces) to cheese_frontend_v2.json (52 products: 50 numeric / 2 null) + yogurts_frontend_v2.json (11: 6 numeric / 5 null), matched by barcode, cross-checks reproduced (cottage 1% che-7290014758681 = 0.6; both capped 9% cottages che-4127336/che-41452 = 5.4). Frontend added satFat to BariNutritionVM (optional `satFat?` — required broke tsc on every corpus lacking the field; render behavior identical since the grid hides null/undefined alike) + a NUTRIENT_LABELS row 'שומן רווי' (ג') after 'שומן' in expansion-section.tsx. CC close-readiness gate: git diff confirms the ONLY semantic change across all 4 files is the satFat additions + the VM/label rows — zero score/grade/insightLine/signal drift (the single -}/+} is a trailing-newline artifact). tsc+build+lint clean, 34 routes incl. /hashvaot/cheese + /hashvaot/yogurts. Resolves the TASK-168H open governance item (verdicts cite sat-fat as the A->B cap reason; the number is now visible in the table)."
summary: >
  Owner approved (2026-06-03) surfacing saturated fat in the displayed nutrition block on the
  cheese + yogurt comparison pages. Resolves the TASK-168H open governance item: cheese verdicts
  cite sat-fat as the A->B cap reason (e.g. "מוצג כ-B ולא A רק בגלל השומן הרווי: 5.4 גרם") and
  2 yogurt verdicts cite it too, but the nutrition table the shopper opens doesn't show it.
  Data: add nutrition.satFat (grams) to cheese_frontend_v2.json + yogurts_frontend_v2.json from
  the authoritative run_cheese_004 / run_yogurt_004 traces (fat_saturated_g), matched by id/barcode,
  null where genuinely absent, NO invention, NO score/grade change. Frontend: add satFat to
  BariNutritionVM + a NUTRIENT_LABELS row ("שומן רווי", ג') after fat in expansion-section.tsx.
  QA: build + spot-check rows render with correct values + zero score/grade drift.
---

# TASK-168J — Surface saturated fat in the cheese + yogurt nutrition table

## Context
TASK-168H closed leaving one owner decision: sat-fat is cited in 25 cheese + 2 yogurt verdicts
(true, from traces) but is **outside** the displayed nutrition block, so a shopper can't verify the
number the verdict leans on. Owner ruling (2026-06-03): **surface saturated fat** (vs. amending the
guide to stop citing it). Display/data only — engine scores are untouched (invariants protected).

## Field contract (Data + Frontend must match)
- VM key = `satFat` (camelCase, consistent with `energyKcal`/`sodium`), type `number | null`,
  placed after `fat` in `BariNutritionVM` (src/lib/view-models/index.ts).
- Display row in `NUTRIENT_LABELS` (src/components/shared/expansion-section.tsx), after `fat`:
  `{ key: "satFat", label: "שומן רווי", unit: 'ג\'' }`. The component already hides null cells.
- Data source = the saturated-fat figure already used by the scoring engine
  (`L1_observed_signals.fat_saturated_g` in run_cheese_004 / run_yogurt_004 traces). Same number,
  no rounding beyond display convention; null where the trace genuinely lacks it (fail-open).
