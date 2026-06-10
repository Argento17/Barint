---
id: TASK-128B
title: Implement Maadanim v2 proof slice (Phase 1)
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "The implementation is complete, verified, and only activation is gated by external sign-offs."
blocker: "CLOSED — implementation complete + verified. B1 CLEARED 2026-06-01 (§14 sign-off + §12 conditions). Slice ships behind MAADANIM_V2_SLICE=false. Consumer ACTIVATION (flip flag → true + QA re-baseline at mobile+lg) is held by TASK-128C (maadanim corpus confidence finalization), not by this task: 87/90 rows ship `verified` incl. 3 instability survivors, which row-level confidence would amplify. Controller decision 2026-06-01: hold activation until 128C closes."
depends_on: [TASK-128]
blocks: []
category_id: null
summary: >
  Implement Maadanim v2 proof slice (Phase 1)
---

# TASK-128B — Implement Maadanim v2 proof slice (Phase 1)

## Scope (as assigned, frontend-agent)
Smallest working v2 slice on **Maadanim only**: extend `BariProductVM`
(`metrics.protein_g`, `rowReason`); promote confidence from footnote to row;
implement protein metric block + strongest +/− reason + disclosure de-dup.
Constraints honored: no `base_pct`, no histogram, no Phase-2 desktop chrome
(rail/dividers), no Wave-2 work.

## Status — IMPLEMENTED, ship BLOCKED on B1 sign-off
The proof slice is fully built, lint-clean, build-green, and verified with
screenshots (mobile + desktop, collapsed + expanded). It is held **dormant behind
`MAADANIM_V2_SLICE` (currently `false`)** in `maadanim-page-data.ts`.

**Why still BLOCKED (registry-authoritative, surfaced not overridden):** ship is
gated on `comparison_ui_reference_v2.md` §14 sign-off (design/product countersign +
Controller acceptance) and §12 open conditions — TASK-106 confirmation, hummus
confidence re-audit, QA re-baseline at mobile + `lg`. frontend-agent cannot clear
this gate. Activation = flip the flag to `true` (one line) once the gate clears.

**Deviation surfaced:** reference §11 names *hummus* as migration order 1 (pilot)
and maadanim as order 2. This task was assigned against Maadanim as a proof slice
(spike) to de-risk and size the fleet rollout — not the gated production pilot.

## Files changed (all under `bari-web/`)
- `src/lib/view-models/index.ts` — `BariProductMetricsVM`, `BariRowReasonVM`, optional `metrics`/`rowReason` on `BariProductVM`.
- `src/lib/comparisons/maadanim-page-data.ts` — `MAADANIM_V2_SLICE` flag + Maadanim-scoped derivation of `metrics.protein_g` and short-form `rowReason`.
- `src/components/shared/metric-block.tsx` — NEW `ProteinMetric` (0–20 g scale, good ≥10 / poor <5, null→"—").
- `src/components/shared/confidence-indicator.tsx` — NEW `ConfidenceIndicator` (dot + pill variants).
- `src/components/shared/product-row.tsx` — `v2Slice` prop: row reason, protein metric, promoted confidence, `confidencePromoted` to expansion, no scrollIntoView under v2.
- `src/components/shared/product-table.tsx` / `src/components/comparisons/comparison-shelf-page.tsx` — thread `v2Slice`.
- `src/components/shared/expansion-section.tsx` — `confidencePromoted` de-dups the confidence footnote.
- `src/components/comparisons/bari-product-shelf-row.tsx` — desktop v2 surface; inline technical (drops 2nd "advanced" toggle), de-dups footnote.
- `src/components/comparisons/bari-comparison-desktop-page.tsx` — thread `v2Slice`.
- `src/components/comparisons/maadanim-comparison-page.tsx` — passes `MAADANIM_V2_SLICE` to both render paths.
- Verification: `scripts/shot-maadanim-v2-128b.mjs`, `scripts/shot-maadanim-v2-128b-crop.mjs`; screenshots in `02_products/maadanim/reports/128b_screenshots/`.

## Verification
- `npm run lint` — 0 errors (pre-existing warnings only, none in changed files).
- `npm run build` — TypeScript clean, all 33 routes generated.
- Maadanim-only confirmed: only `maadanim-comparison-page.tsx` passes the flag;
  hummus regression screenshot shows the other categories unchanged.

## Proposed next state
Remains **BLOCKED** until B1 (§14 sign-off + §12 conditions) clears. Only the
Central Controller records CLOSED; on gate-clear, flip `MAADANIM_V2_SLICE` and
hand to QA for the mobile + `lg` re-baseline.
