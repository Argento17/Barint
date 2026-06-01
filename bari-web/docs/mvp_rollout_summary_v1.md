# Bari Four-Category MVP Rollout — Summary v1

**Date:** 2026-05-30  
**Scope:** Milk, Snacks, Bread, Yogurts at ~70% MVP readiness

---

## Status

| Category | Route | Status |
|---|---|---|
| Milk | `/hashvaot/milk-comparison` | Live — reference template; no schema migration |
| Snacks | `/hashvaot/snacks` | Live — shared desktop template + v2 corpus |
| Bread | `/hashvaot/bread` | Live — shared template; handoff copy applied; grade audit |
| Yogurts | `/hashvaot/yogurts` | Live — new MVP corpus + shared template |

Index (`/hashvaot`): Milk (recommended), Bread, Snacks, Yogurts.

---

## What was implemented

### Snacks & Bread (verification + alignment)

- Confirmed split mobile/desktop via `BariComparisonDesktopPage`
- Bread hero, prologue, methodology updated per `bread_comparison_mvp_handoff_v1.md`
- Bread metadata line: `N מוצרים נבדקו · מדגם שופרסל · ממוין לפי ציון Bari`
- Grade fix: `לחם ירוק מקמח מלא` score 80 → grade A

### Yogurts (new)

- `src/data/comparisons/yogurts_frontend_v1.json` — 14 products, manual calibrated scores
- Filters: plain, greek, dairy-free, high-protein, flavored
- Full expansion content per handoff template
- Route, page component, registry entry, index intelligence card

### Template standardization

- Documented in `docs/comparison_template_v1.md`
- Shared: layout, components, styling, responsive behavior
- Category-specific: data, lenses, methodology, editorial

### Milk (audit only)

- Route active; custom schema preserved per handoff
- Desktop uses same intelligence hero and shelf row pattern

---

## Files changed (this rollout)

**Created**

- `src/data/comparisons/yogurts_frontend_v1.json`
- `src/lib/comparisons/yogurts-comparison-page-data.ts`
- `src/lib/comparisons/yogurts-shelf-filters.ts`
- `src/components/comparisons/yogurts-comparison-page.tsx`
- `src/components/hashvaot/featured-yogurts-intelligence-card.tsx`
- `src/app/hashvaot/yogurts/page.tsx`
- `src/lib/comparisons/registry/categories/yogurts.ts`
- `scripts/generate-yogurts-corpus.mjs`
- `scripts/fix-bread-grades.mjs`
- `docs/comparison_template_v1.md`
- `docs/mvp_rollout_summary_v1.md`

**Updated**

- `src/lib/comparisons/bread-comparison-page-data.ts`
- `src/components/comparisons/bread-comparison-page.tsx`
- `src/data/comparisons/bread_frontend_v2.json` (grade audit)
- `src/lib/comparisons/registry/types.ts`
- `src/lib/comparisons/registry/index.ts`
- `src/app/hashvaot/page.tsx`

---

## Known limitations

1. **Yogurt images:** MVP corpus uses `imageUrl: null` — thumbnails show placeholder until retail URLs are added.
2. **Yogurt scores:** Manual calibration per handoff; not BSIP2-derived from a full scrape run.
3. **Bread rescore:** Full R-01/R-02/R-03 score bumps (fermentation products → A) were not re-applied to JSON — user stated recalibration approved; only grade/score alignment was verified. Distribution still reflects pre-rescore values except grade fixes.
4. **Milk schema:** Architectural exception — not on `BariProductVM` / registry.
5. **Maadanim:** Route `/hashvaot/maadanim` remains live but removed from four-category index in favor of Yogurts.
6. **Lint:** `npm run lint` may OOM in constrained environments; `npm run build` is the primary gate.

---

## Blockers encountered

None for MVP launch. Post-MVP:

- Yogurt product images (Yochananof/Shufersal URLs)
- BSIP2 re-run for yogurts and full bread rescore if engine outputs differ from manual targets
- Optional: migrate milk to unified `BariProductVM` corpus

---

## QA checklist

- [x] Routes: milk-comparison, snacks, bread, yogurts
- [x] Desktop: shared `BariComparisonDesktopPage` (snacks, bread, yogurts)
- [x] Mobile: `ComparisonShelfPage` preserved
- [x] Methodology sections present (all four)
- [x] Filters/lenses wired (snacks, bread, yogurts)
- [x] Build passes (`npm run build`)
