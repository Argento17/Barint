# Bari Score-Propagation Audit — Synthesis & Action List

## Context

A 4-way parallel read-only audit checked score propagation for `/hashvaot/milk-comparison`, `/hashvaot/snacks`, `/hashvaot/bread`, and `/hashvaot/yogurts`. Goal: confirm scores flow cleanly from the BSIP2-generated JSON to the rendered UI, with no staleness or hardcoding.

**Result: all four PASS.** Scores are read verbatim from a single authoritative JSON per category → corpus loader / page-data → components. No product scores are computed or hardcoded. All website JSONs were regenerated 2026-05-30 (R-01–R-05 recalibration) and match or post-date their `C:\Bari` sources.

This plan is the cleanup/hardening backlog derived from the audit. None of these block correctness today; they are drift vectors that will cause stale or inconsistent data on the *next* regeneration if left unaddressed.

## Audit Summary (per category)

| Category | Route | Data source (website) | Score path | Verdict |
|---|---|---|---|---|
| Milk | `/hashvaot/milk-comparison` | `src/data/milk-comparison.json` (legacy flat path) | JSON → `milk-page-data.ts` (typed cast) → `MilkComparisonPage` → `BariGradeBadge` (`Math.round`) | PASS |
| Snacks | `/hashvaot/snacks` | `src/data/comparisons/snacks_frontend_v2.json` | JSON → `loadComparisonCorpus` → `BariProductVM[]` → `bari-product-shelf-row` | PASS |
| Bread | `/hashvaot/bread` | `src/data/comparisons/bread_frontend_v2.json` | JSON → `loadComparisonCorpus` → `BariProductVM[]` → canonical shelf/desktop | PASS |
| Yogurts | `/hashvaot/yogurts` | `src/data/comparisons/yogurts_frontend_v1.json` | JSON → `loadComparisonCorpus` → `BariProductVM[]` → `bari-product-shelf-row` | PASS |

Overlapping routes are safe: `/hashvaot/snack-bars`, `/compare/snack-bars`, `/hashvaot/bread-comparison` all `redirect()` to canonical hrefs; `/categories/snacks` returns `notFound()`.

## Action List (prioritized)

### P1 — Drift vectors that will reintroduce stale data on regeneration

1. **Normalize milk onto the versioned `comparisons/` convention.** Milk is the only category reading the legacy flat path `src/data/milk-comparison.json` and has no committed build script in `C:\Bari` (`02_products/milk_and_alternatives/comparisons/` is empty). Move to `src/data/comparisons/milk_frontend_vN.json` + a generator matching maadanim/bread.
   - Files: `src/data/milk-comparison.json`, `src/lib/comparisons/milk-page-data.ts`
   - Owner: Frontend Architect (website wiring) + Chief Nutrition Officer (confirm source run)

2. **Neutralize deprecated generator scripts** that would overwrite recalibrated JSON from stale fixtures if run.
   - `C:\Users\HP\bari\scripts\build-snacks-frontend-v2.ts` (regenerates from legacy fixture order, drops CE recalibrations)
   - Action: confirm not wired into `package.json` build; consider removing or gating behind an explicit guard.
   - Owner: Frontend Architect

### P2 — Hardcoded display values (not product scores, but visible drift)

3. **Snacks hardcoded top score `70/B` in prose** — `src/lib/comparisons/snacks-comparison-page-data.ts:67` and `src/components/comparisons/snacks-comparison-page.tsx:36`. Will mislead if the top score changes.
   - Owner: Frontend Architect

4. **Bread `BREAD_REPORT_STATS`** (scanned 256 / sufficient 81 / etc.) hardcoded in `src/lib/comparisons/bread-page-data.ts`, consumed by the active hero. Decouple from prose or derive from the dataset.
   - Owner: Frontend Architect

### P3 — Architectural smell (future divergence)

5. **Dual page-data files per category.** Bread mixes canonical `bread-comparison-page-data.ts` (scores from v2) with legacy `bread-page-data.ts` (stats). Snacks keeps legacy `snack-page-data.ts` for hero stats. Both currently in sync; consolidate to a single source per category to prevent silent divergence.
   - Owner: Frontend Architect

### P4 — Verify intentional curation (informational)

6. **Confirm curated subsets are intentional**, not accidental drops:
   - Milk: 18 shown vs 20 in `run_004_recalibrated` (top scores align; 2 dropped editorially)
   - Yogurts: 14 shown vs 45 in `run_yogurt_001`
   - Owner: Chief Nutrition Officer (curation decision) → QA & Audit Lead (record expected counts)

## Verification

- After any P1/P2/P3 change: `npm run build` and `npm run lint` in `C:\Users\HP\bari`; load each `/hashvaot/*` route and confirm the top product's chip matches the JSON `score`/`grade`.
- Re-run this 4-category propagation audit (trace JSON `score` → rendered chip) to confirm no regression.
- For milk normalization: confirm the new `comparisons/milk_frontend_vN.json` `_meta.source_run_id` points at `run_004_recalibrated` and product scores match the source for all retained products.

## Note

This plan is a remediation backlog produced from a read-only audit. No fixes have been applied. Nothing here is a current correctness failure — all four categories propagate scores correctly today.
