---
status: CLOSED
priority: medium
owner: content-agent
created: 2026-06-10
updated: 2026-06-10
closed: 2026-06-10
category: editorial
roadmap_impact: false
tags: [copy, hebrew, framework-invisibility, snack-bars, nova, governance]
supersedes: []
superseded_by: []
ancestry: "TASK-BARI-COPY-LEAK-YOGURT-NOVA-V1 — audit of other comparison pages found snack-bars NOVA leak"
close_reason: >
  Reworded NOVA out of the live snack-bars comparison page + flagship blog, mapping the
  NOVA scale to plain consumer Hebrew (NOVA2→עיבוד מינימלי, NOVA3→עיבוד בינוני,
  NOVA4→עיבוד עמוק) and removing two banned phrases (בסיס מהונדס→בסיס מורכב;
  ריבוי ממתיקים→מקורות מתיקות מרובים). Files: snack-editorial-content.ts (blog, 6 edits),
  snack-product-detail.ts (component labels via display-mapping, no data/score change),
  filter-panel.tsx (NOVA header + buttons → עומק עיבוד / מינימלי·בינוני·עמוק via a label
  map). Processing-depth argument + comparative spread preserved; no scores/data changed.
  Verified: no consumer-rendered NOVA/banned phrase remains (only code identifiers
  SnackNOVA/NOVA_OPTIONS + a "never rendered" comment); run_d3_ci.py 7/7 GREEN.
  OUT-OF-SCOPE finding (NOT fixed): app/products/demo/page.tsx:783 renders "NOVA … 4" —
  a demo/dev page, not a comparison page. Frontend build/typecheck not run locally
  (changes are type-safe string/label edits) — confirm on first PR CI.
---

# TASK-BARI-COPY-LEAK-SNACKBARS-NOVA-V1: Reword NOVA out of snack-bars consumer copy

## Objective
Remove literal `NOVA`/`NOVA2/3/4` and the banned phrase `בסיס מהונדס` from the LIVE
snack-bars comparison page + flagship blog, while PRESERVING the editorial argument
("processing depth caps the score regardless of marketing/name"). Express the NOVA
scale in plain consumer Hebrew using the existing frame `עומק עיבוד` / `רמת עיבוד`
(minimal / moderate / high–deep), per consumer_explanation_view sanitization style.

## Scope (live snack-bars surfaces)
- `bari-web/src/lib/comparisons/snack-product-detail.ts`
- `bari-web/src/lib/blog/snack-editorial-content.ts`
- `bari-web/src/components/snack/filter-panel.tsx` (NOVA filter label)

## Constraints
- No scoring/data changes. No score values changed.
- Keep consumer meaning + the comparative spread intact.
- No new banned phrases; no other framework terms.

## DoD
1. [x] All NOVA / `בסיס מהונדס` / `ריבוי ממתיקים` in the 3 surfaces reworded to plain Hebrew.
2. [x] Processing-depth argument + comparative spread preserved (minimal/moderate/deep scale).
3. [x] No consumer-rendered framework term / banned phrase remains (grep clean; only code identifiers left).
4. [x] run_d3_ci.py 7/7 green (no governance-gate regression).

## Out-of-scope finding (NOT fixed)
- `app/products/demo/page.tsx:783` renders "NOVA … 4" — demo/dev page, not a comparison page.
