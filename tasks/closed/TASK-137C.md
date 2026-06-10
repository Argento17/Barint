---
id: TASK-137C
title: "Frontend: replace collapsed-row +/- with a 2-3 sentence rowVerdict (shared VM + row component; +/- stays inside the expansion)"
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: [TASK-137D]
category_id: hummus
summary: >
  Add rowVerdict?: string to BariProductVM. In bari-product-shelf-row, remove DesktopRowReason (+/- under the name) from the collapsed v2 row and render rowVerdict instead; positiveSignals/limitingFactors remain inside the 'למה קיבל את הציון?' expansion (already there). Shared component => change is once and propagates to all v2 categories. Design sign-off on the new row density.
---

# TASK-137C — Frontend: replace collapsed-row +/- with a 2-3 sentence rowVerdict (shared VM + row component; +/- stays inside the expansion)

## Done (editorial hero/prologue fixes — Product directive 2026-06-01)
1. Removed the "ממרחי ירקות … בדף נפרד" prologue line (data file).
2. Added `showInsights?: boolean` (default true) to `ComparisonIntelligenceHero`; hummus passes
   `showInsights: false` → the "תובנות מרכזיות" rotating-insight box no longer renders on the
   hummus hero. **Scoped to hummus** (other live categories keep the box until 137E decides).
3. Prologue restyled in `bari-comparison-desktop-page.tsx`: right-aligned (removed `mx-auto`) and
   higher-contrast (`text-[#4E5663]` → `#2A2F36`). **Shared component — also affects maadanim/bread/
   snacks/yogurts desktop prologues** (intended standardization direction; flagged to Product).

## Done — core 137C scope (2026-06-01)
- `rowVerdict?: string` added to `BariProductVM` (display-only; loader passes it through via `...rest`).
- `bari-product-shelf-row.tsx`: collapsed v2 row now renders `rowVerdict` (2–3 sentences) in place of
  `DesktopRowReason` (+/−); falls back to +/− only where no verdict is authored. The full +/− still
  renders inside "למה קיבל את הציון?".
- 35 verdicts injected **directly into** `hummus_frontend_v3.json` (live + workspace copies) — 137D's
  builder path was closed as "not necessary". Clean additive diff; typecheck green; 35/35 present.
- **Hero box killed for hummus** (`showHeroCard={false}` on `BariComparisonDesktopPage`) — it
  duplicated the `/hashvaot` `FeaturedHummusIntelligenceCard`. Replaced with a lightweight H1 title.
- "תובנות מרכזיות" box off for hummus (`showInsights={false}`); prologue restyle approved.

## Pending review
Design sign-off on row density (2–3 sentence verdict per row lengthens the list — per Product
directive). QA (rolled into 137E gate). RETURNED for Controller close.
