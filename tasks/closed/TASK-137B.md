---
id: TASK-137B
title: "Content: rewrite hummus prologue (what/how/why-protein) + author 2-3 sentence editorial verdict per displayed product"
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: [TASK-137A]
blocks: [TASK-137D]
category_id: hummus
summary: >
  Rewrite hummusPrologueSentences so the reader learns WHAT was measured, HOW it was measured, and WHY protein is the headline metric (grounded by Nutrition's rationale). Author a 2-3 sentence 'our opinion of the product' verdict for each displayed hummus product, to render on the collapsed row in place of the +/- lines. Tone per assertive-writing + insight-line specs; no per-grade boilerplate.
---

# TASK-137B — Content: rewrite hummus prologue (what/how/why-protein) + author 2-3 sentence editorial verdict per displayed product

## Deliverable
`02_products/hummus/content/hummus_row_verdicts_137B.md`

## Done (LIVE)
- **Prologue rewritten** (what / how / **why protein** + guardrail + fat caveat + scope) — wired in
  `hummus-comparison-page-data.ts` (`hummusPrologueSentences`). Renders immediately.
- **Insight lines refreshed** in `hummus-comparison-page.tsx` — removed the stale "פער 37 נקודות"
  (real range 80→63), now reflects the homogeneous-cluster story (1 A; most 63–71; tahini+additives
  are the differentiator).

## Done
- **Row verdicts: all 35 authored** (pattern approved by Product 2026-06-01), keyed by id in the
  deliverable. 2–3 sentences each, finding-first, grounded only in each product's trace; no
  invented data; no per-grade boilerplate.

## Hand-off
137C wires `rowVerdict` to the VM + row (removing the +/− from the row face); 137D stages the
strings into `hummus_frontend_v3.json` and syncs to bari-web.

## State
137B deliverable complete. **Proposing RETURNED** (only the Central Controller records CLOSED).
