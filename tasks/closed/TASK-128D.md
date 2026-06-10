---
id: TASK-128D
title: Roll out Phase-1 v2 slice to Hummus
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: [TASK-128, TASK-128B]
blocks: []
category_id: null
summary: >
  Roll out Phase-1 v2 slice to Hummus (the migration-order-1 pilot, comparison_ui_reference_v2 §11)
  by reusing the generic v2Slice machinery proven on Maadanim (TASK-128B). Implementation complete,
  lint/build green, verified at mobile 375 + lg 1280 (collapsed + expanded). Shipped DORMANT behind
  HUMMUS_V2_SLICE=false; consumer ACTIVATION (flip flag + QA re-baseline) is Controller/QA-gated.
---

# TASK-128D — Roll out Phase-1 v2 slice to Hummus

## Scope (as assigned, frontend-agent)
Apply the Phase-1 v2 slice to Hummus, reusing the Maadanim implementation (TASK-128B).
Constraints honored: **reuse Maadanim impl** (the `v2Slice` shared machinery is reused
**unchanged** — no shared component edited), **no new UI concepts**, **no `base_pct`**,
**no Phase-2 chrome** (no rail / dividers / histogram).

## Status — IMPLEMENTED + VERIFIED, shipped DORMANT (activation gated)
Proof: lint 0 errors (9 pre-existing `<img>` warnings only), `npm run build` green (33/33
routes incl. `/hashvaot/hummus`), screenshots captured at mobile 375 + lg 1280, collapsed
+ expanded, with the flag flipped `true`. Committed state holds `HUMMUS_V2_SLICE = false`.

## Files changed (TASK-128D, all under `bari-web/`)
- `src/lib/comparisons/hummus-comparison-page-data.ts` — `HUMMUS_V2_SLICE` flag +
  `shortenReason` + `enrichHummusV2Slice` (derives `metrics.protein_g` from
  `expansion.nutrition.protein`; `rowReason` from `positiveSignals[0]`/`limitingFactors[0]`).
  Display-only; no score/corpus change. Mirrors `maadanim-page-data.ts` verbatim.
- `src/components/comparisons/hummus-comparison-page.tsx` — import `HUMMUS_V2_SLICE`;
  thread `v2Slice` into both the mobile (`ComparisonShelfPage`) and desktop
  (`BariComparisonDesktopPage`) render paths.
- NEW `scripts/shot-hummus-v2-128d.mjs`, `scripts/shot-hummus-v2-128d-crop.mjs` — verification.

**Reused unchanged from TASK-128B** (genuine reuse, zero edits): `view-models/index.ts`
(`metrics`/`rowReason`), `metric-block.tsx` (`ProteinMetric`), `confidence-indicator.tsx`,
`product-row.tsx`, `product-table.tsx`, `comparison-shelf-page.tsx`,
`bari-comparison-desktop-page.tsx`, `bari-product-shelf-row.tsx`, `expansion-section.tsx`.

## Verification artifacts
`02_products/hummus/reports/128d_screenshots/` — `mobile-collapsed.png`,
`mobile-expanded.png`, `mobile-expanded-top.png`, `desktop-collapsed.png`,
`desktop-expanded.png`. All four canonical v2 surfaces confirmed on hummus: protein bar,
promoted confidence pill, short +/− row reason, restructured expansion (no 2nd advanced
toggle, `הקשר במדף`/section identity intact, no `scrollIntoView` on expand).

## Rollout BLOCKER for ACTIVATION (frontend cannot clear — Controller/Data/QA)
Promoting confidence to the row header **amplifies the TASK-129 re-audit P0 #1 defect**:
the presence-based `verified` gate over-labels **~15 hummus marketing-prose rows** (58/66
displayed are `verified`). TASK-129 §5 rates hummus 🟢 GO and lists the `verified→partial`
relabel as a carry-forward "without blocking" — but that relabel was sized against the v1
10px footnote, **not** a headline row label. This is the hummus analogue of the maadanim
gate (TASK-128C). Recommend: confidence-gate hardening (re-audit P0 #1) OR explicit
Controller acceptance of the carry-forward **before** flipping `HUMMUS_V2_SLICE`.

## Proposed next state
**RETURNED** — deliverable complete + verified. Activation = flip `HUMMUS_V2_SLICE = true`
(one line) + QA re-baseline at mobile + `lg`, recorded by the Central Controller, after the
activation blocker above is dispositioned. Only the Controller records CLOSED.
