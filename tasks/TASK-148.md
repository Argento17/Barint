---
id: TASK-148
title: "Unify the /hashvaot comparison tables into one responsive ComparisonPage (design handoff IMP-1…6)"
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
closed_at: 2026-06-02
closed_by: cc-agent
depends_on: []
blocks: []
category_id: null
summary: >
  Consolidation of the divergent /hashvaot comparison-table code per the design handoff
  (C:\Bari\design\new_design_proposal.zip). Collapses four divergent renderers into ONE
  responsive ComparisonPage: a single container-query ComparisonRow/Table (phone↔desktop
  via CSS, not a second component) carrying the v2 surface (aligned metric column, in-list
  band dividers, scroll-only band rail, promoted confidence). Replaces both the phone-frame
  ComparisonShelfPage and the bespoke BariComparisonDesktopPage; deletes the dead web-grid
  path. IMP-1…6 ALL COMPLETE (verified tsc+lint+build+visual QA, 2026-06-02): all 7 routes incl.
  milk migrated onto the one ComparisonPage, legacy chain deleted, hummus category-note once. No
  frontend work remains. Pending CLOSE only on governance re-approval of 2 retired surfaces
  (decisions #2 desktop chrome, #4 milk pillars — Content/Nutrition/Design call). Frontend-only;
  NO scores/scoring touched.
---

# TASK-148 — Unify the /hashvaot comparison tables (design handoff IMP-1…6)

Frontend consolidation driven by the design bundle at `C:\Bari\design\new_design_proposal.zip`
(`README.md` migration plan, `MILK_RECOMMENDATION.md`, `comparison-v2-spec.md`, the audit +
One-Table prototype). The audit found the seven comparison tables had drifted into three
experiences (D1 milk parallel table, D2 separate mobile/desktop components, D3 v2 row on only
2 of 6, D4 a dead desktop web-grid path). Target: categories differ only in **data**, never layout.

**Hard boundary:** website-only. No published score, scoring rule, or corpus content changed.

## Done (verified: `tsc --noEmit` ✓, `eslint` ✓, `next build` ✓ all 31 routes, Playwright visual QA at 1280px + 390px)

- **IMP-5 — deleted the dead web-grid path:** removed `product-table-header.tsx`,
  `comparison-layout-context.tsx`, the `isWeb`/`layout="web"` branches, orphaned `webTable`
  tokens + `comparisonWebTableGridClass`, and dead `bari-zebra-rows--web` CSS. Was unreachable
  in production (no page passed `layout="web"`).
- **IMP-1 + IMP-4 (core) — one responsive table:** new `comparison-row.tsx` + `comparison-table.tsx`
  reflow phone↔desktop on identical DOM via a `@container bari-cmptable` query (CSS in `globals.css`,
  prefixed `.bari-cmp-*`). Carries: category-configurable aligned **MetricColumn**
  (`comparison-metric-column.tsx`), in-list **band dividers** + scroll-only **band rail**
  (`comparison-bands.ts`, `scrollTo` not `scrollIntoView`), promoted confidence. New
  `comparison-page.tsx` shell replaces both `ComparisonShelfPage` and `BariComparisonDesktopPage`.
  Primitives consolidated onto `BariGradeBadge` + `BariProductThumbnail` (container-responsive
  thumbnail: 56px mobile → 80px desktop via a `size="fill"` mode).
- **IMP-2 — v2 is the only path:** `v2Slice` flag removed; hummus/maadanim always enrich the row
  surface (`enrich*RowSurface`).
- **All 6 categories migrated** to `ComparisonPage`: hummus + maadanim show the protein metric
  (their editorial headline); yogurts/snacks/spreads/bread render with no metric column (fall back
  to their existing `insightLine` — content preserved). Blog-link CTAs preserved (snacks, bread).
- **Legacy chain deleted:** `comparison-shelf-page.tsx`, `bari-comparison-desktop-page.tsx`,
  `bari-product-shelf-row.tsx`, `product-table.tsx`, `product-row.tsx`, `metric-block.tsx`.
- **Expansion regression fixes** (it's now table-only): nutrition renders as adjacent label+value
  pairs (was `justify-between` → flung to edges at table width); expansion inset under the name
  column with a capped reading width.
- **IMP-3 — Milk folded in:** `milk-comparison-page.tsx` is now a thin `ComparisonPage` wrapper
  (mirrors `hummus-comparison-page.tsx`); the bespoke inline `ProductShelfRow`, framer-motion row,
  4-cell grid and `ComparisonIntelligenceHero`/`HomeContainer` chrome are gone. New
  `milk-comparison-page-data.ts` reshapes the bespoke `MilkComparisonProduct` into `BariProductVM`
  via `buildConsumerExplanationView` (all copy verbatim): `raisesScore`→`positiveSignals`,
  `lowersScore`→`limitingFactors`, `relativeToPeers`→`comparisonContext`, `tradeoffNote`→`caveats`.
  All 18 milk products are curated (milk-product-insights), so the authored `whatToKnow`
  (analysis) + `takeawayLine` (verdict) are composed into a **`rowVerdict`** — a 2-sentence
  collapsed-row description matching the maadanim row treatment (the operator flagged that milk
  rows lacked the per-product "what we saw in the analysis" sentences that maadanim shows; terse
  +/− reason lines were the wrong call here). New `milk-shelf-filters.ts` adapts the type/trait
  filter set onto the shared `ComparisonShelfFilters` contract (filters out non-matching rather
  than dimming, like every other category). Metric column = **protein + sugar**
  (`DAIRY_PROTEIN_METRIC` added — per-100ml scale max 8 / good 5 / poor 2, honest aria unit;
  reuses `SUGAR_METRIC`). Only shared-component change is that new metric preset; `ExpansionSection`
  + the VM are otherwise untouched by IMP-3. Blog link + prologue + methodology preserved. Scores
  untouched (top milk still 85/A whole/4%, per the frozen milk invariant).
- **IMP-6 — category note once:** the hummus fat-data caveat now renders **once** in the header
  `categoryNote` slot; removed from prologue (former sentence 5) and the methodology footer (the
  short duplicate). Wired `categoryNote` through `HummusComparisonPage` → its route.

## Decisions / constraints (governed — surface for review)

1. **Metric column is honest, not the prototype's 3 metrics.** Source frontend JSON has NO
   `additive_count` or `base_pct`; fabricating them violates the "don't invent ingredient data"
   rule. Shipped **protein-only** (hummus/maadanim) — which is also their prologue headline — and
   **no metric** for the other 4. VM contract (`view-models/index.ts`) carries optional
   `additive_count` / `base_pct` / `sugar_g` slots. **→ Data Agent / BSIP dependency** to expose
   additives + main-ingredient % into the frontend JSON before those metrics can ship.
2. **Desktop editorial chrome retired** per operator decision (full-unification): the
   `ComparisonIntelligenceHero` card + "מנוע השוואה" section + back-link are gone, replaced by the
   shared responsive chrome. Prologue/methodology copy preserved verbatim. **→ Content/Design may
   want to re-approve** the desktop presentation of the canonical (maadanim) reference page.
3. **Headline metric for yogurts/snacks/spreads/bread is intentionally unset** — that's a
   Content/Nutrition call, not a frontend assertion.
4. **Milk's "advanced — פירוט לפי היבטים" pillars panel was NOT ported (IMP-3).** It is a
   per-dimension score-bar + strength-label (חזק/בינוני/חלש) surface — both are deprecated **Gen-0**
   patterns (Architecture Generations Registry: "dimension bars", "score attribution") and the
   strength labels are explicitly **forbidden** by the Score Presentation rules. No other category
   exposes pillars; adding a slot for them to the shared expansion would re-introduce exactly the
   category-specific divergence this unification removes. Also dropped: the two **textual** grid
   cells (תוספים label, רכיב עיקרי) — they aren't numeric metrics and their content is already
   narrated in the positive/limiting signal lines; and the brand subtitle (`brandLine`), since no
   category's unified row carries a brand line. **→ Content / Nutrition / Design: please re-approve**
   the dropped pillars view (parallels decision #2).

## Exit / DoD

All 7 comparison routes (incl. milk) render through one responsive `ComparisonPage`; no
category-specific row/page component remains; metric set is category-config (only real data shown);
corpus order + every-product-visible invariants hold; tsc+lint+build green; mobile + desktop visual
QA re-baselined. Then propose RETURNED (CC records CLOSED).

## Log

- 2026-06-01: Opened. IMP-5/1/2/4-core complete + 6 categories migrated + legacy deleted + expansion
  fixes + thumbnail enlargement (56/80px). Verified green. Nothing committed yet. IMP-3 + IMP-6 pending.
- 2026-06-02: IMP-3 (Milk folded onto `ComparisonPage`) + IMP-6 (hummus category-note once) complete.
  All 7 comparison routes now render through the one responsive `ComparisonPage`; no
  category-specific row/page component remains. Verified: `tsc --noEmit` ✓, `eslint` ✓ (0 errors,
  9 pre-existing warnings), `next build` ✓ (33 routes incl. `/hashvaot/milk-comparison`), Playwright
  visual QA at 390px + 1280px (milk collapsed/expanded — protein+sugar metrics with null sugar→"—",
  band rail, promoted confidence, lead→positives→limits→bottom-line→shelf-context expansion; hummus
  note box renders once at both widths, expansion unaffected). One governed decision logged
  (#4: milk pillars panel dropped) for Content/Nutrition/Design re-approval. Nothing committed.
  **Proposing RETURNED** (CC to record CLOSED).
- 2026-06-02 (follow-up): operator review caught that milk rows showed only terse +/− clauses while
  maadanim rows carry an authored 2–3 sentence verdict. Milk is fully curated, so reworked IMP-3 to
  compose the authored analysis + verdict into `rowVerdict` (now matches maadanim); reverted the
  short-lived `expansion.lead` field/rendering (no longer needed → no dead code). Re-verified
  tsc/lint/build green + visual QA at 390/1280. Still RETURNED.

---

## CLOSED (2026-06-02, cc-agent — close-readiness gate PASS)

**Implementation verified against artifacts (not trusted from the return block):** new responsive
primitives exist (comparison-row.tsx, comparison-table.tsx, comparison-metric-column.tsx,
comparisons/comparison-page.tsx); milk-comparison-page.tsx is a thin ComparisonPage wrapper +
milk-comparison-page-data.ts present (IMP-3); categoryNote wired hummus route -> comparison-page (IMP-6);
all 6 legacy files + dead web-grid files confirmed DELETED. CC re-ran `tsc --noEmit` -> exit 0.

**Governance re-approval obtained (the only gate on CLOSE):**
- Design sign-off — APPROVE both (#2, #4). Retired maadanim chrome not part of the frozen 4-section
  canonical contract (Hero/Prologue/Table/Methodology preserved); dropping the milk pillars panel is
  required, not merely tolerable (dimension bars + score-attribution = deprecated Gen-0; strength labels
  forbidden by Score Presentation).
- Content sign-off — APPROVE both (#2, #4). Maadanim prologue (5) + methodology (4) render verbatim;
  retired insight card still lives on the /hashvaot index teaser; milk additives/main-ingredient facts
  confirmed remapped into curated signal lines; reworked rowVerdict reads clean.

**Residuals (non-blocking, carried forward):**
- Decision #1 (3-metric column: additive_count + main-ingredient %) is a future Data Agent / BSIP
  dependency to expose those fields into frontend JSON; VM slots reserved. No open task yet.
- Content flagged one milk SKU (koos 7290014760141) whose lecithin/stabilizer label isn't mirrored in
  its curated cautions — optional Nutrition polish, no factual loss.
- Working-tree changes uncommitted (as with the other 2026-06-02 swaps).

All 7 /hashvaot routes render through one responsive ComparisonPage; no scores/scoring touched. CLOSED.
