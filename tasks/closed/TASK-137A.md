---
id: TASK-137A
title: "Nutrition: protein-as-headline rationale for hummus + category-boundary ruling on the three 'סלט' items (spread vs salad)"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: [TASK-137B, TASK-137D]
category_id: hummus
summary: >
  Deliver the why-protein rationale that feeds the new prologue (why protein is the decisive consumer signal for hummus). Rule per-product whether each 'סלט'-named item is a prepared spread or a chickpea salad that does not belong on the spreads shelf: bsip1_6666307 'סלט חומוס' (80/A, whole-bean salad image), bsip1_7296073725374 'סלט חומוס עם טחינה', bsip1_7296073005... 'סלט חומוס+מסבחה' (masabacha). Output an exclude/keep decision + one-line reason each for the Data audit record.
---

# TASK-137A — Nutrition: protein rationale + 'סלט' boundary ruling

## Deliverable
`02_products/hummus/launch/hummus_salad_boundary_ruling_137A.md` — full ruling + rationale.

## Ruling (FINAL — corrected discriminator)
**Boundary test = is it a prepared spread, or raw/dry chickpeas?** Markers: tahini present,
sodium 300–480 mg, energy 250–290 kcal = prepared (KEEP). No tahini, sodium ~12 mg, energy
380 kcal = raw/dry chickpeas (EXCLUDE). **Protein alone is NOT a boundary signal** (a thick
tahini salad legitimately hits ~18 g).
- **EXCLUDE** `bsip1_1990261` + `bsip1_3643714` — both "חומוס" 73/B, sodium 12 mg, energy 380
  kcal, no ingredient list, no tahini → raw/dry chickpeas mis-tagged `hummus_spread`. Implemented
  as `EXCLUDED_RAW_CHICKPEA_IDS` in `hummus-comparison-page-data.ts`.
- **KEEP** all tahini-based salads/spreads incl. `bsip1_6666307` "סלט חומוס" 80/A (Product Owner:
  "DO NOT EXCLUDE HUMUS SPREADS/SALAD"). An earlier draft wrongly proposed excluding it on a
  protein-only read — corrected; protein is not a boundary test.
- Impact: 37 → **35** displayed, grade-A **1** (unchanged), range 80→63. Counts auto-derive.

## Why-protein rationale (for 137B prologue)
Protein = category's defining contribution + proxy for real-food fraction vs. water/oil dilution +
the most trustworthy number we can show (fat is suppressed in this corpus) + consumer-legible.
Guardrail: protein is the headline, not the whole score.

## State
Protein-headline rationale delivered (feeds 137B). Boundary ruling final: exclude 2 raw-chickpea
items, keep all prepared salads/spreads. Exclusion implemented in `hummus-comparison-page-data.ts`
(`EXCLUDED_RAW_CHICKPEA_IDS`). **Proposing RETURNED** (only the Central Controller records CLOSED).
137B unblocked: prologue keeps "מוצר אחד בציון A" (סלט חומוס stays) and must fix the stale
"פער 37 נקודות" insight line (current range 80→63). 137D: confirm rowVerdict wiring + re-baseline.
