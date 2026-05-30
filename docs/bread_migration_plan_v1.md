# Bread Migration Plan v1

**Status:** Planning only — no implementation.  
**Reference:** `docs/comparison_ui_reference_v1.md`  
**Canonical stack:** `ComparisonShelfPage` → shared category/product primitives  
**Date:** 2026-05-29

---

## 1. Executive summary

Bread today is a **standalone investigative dashboard**, not a shelf comparison on the frozen template. Production traffic resolves to `/compare/bread-comparison` via redirect from `/hashvaot/bread-comparison`. The page uses `BreadProduct`, a wide desktop table, editorial hero blocks, insight cards, pair comparisons, and a transparency archive — none of which exist on the מעדנים reference path.

Migration means **replacing the dashboard with the shelf stack** while preserving pre-authored Hebrew and corpus order. It is primarily a **data contract + route consolidation** project, not a component tweak. Editorial sections that are not in Comparison UI Reference v1 must be **relocated to blog** or **dropped from the comparison route**, not reimplemented inside `ComparisonShelfPage`.

---

## 2. Current bread architecture assessment

### 2.1 Route and entry

| Item | Location | Behavior |
|------|----------|----------|
| Legacy hashvaot redirect | `src/app/hashvaot/bread-comparison/page.tsx` | `redirect` → `BREAD_COMPARISON_HREF` (`/compare/bread-comparison`) |
| Production entry | `src/app/compare/bread-comparison/page.tsx` | Renders `BreadComparisonDashboard` |
| Shufersal alias | `src/app/compare/bread-shufersal/page.tsx` | Same redirect |
| Index link | `src/app/hashvaot/page.tsx` | Featured card → `/compare/bread-comparison` |

Bread is **not** on `/hashvaot/{category}` and **not** in `comparisonCategoryRegistry`.

### 2.2 UI composition (today)

```
/compare/bread-comparison
  → BreadComparisonDashboard
      → ComparisonHero          (animated grid, stats, English eyebrow)
      → Cluster filter chips    (single-select, includes "all")
      → ComparisonTable         (desktop <table>, 6 columns, external links)
      → InsightBlocks           (4 editorial cards)
      → PairCard[]              (3 side-by-side comparisons)
      → TransparencyArchive     (unscored products grid)
      → Methodology <details>   (collapsible, not MethodologyFooter)
```

**Not used:** `ComparisonShelfPage`, `CategoryHero`, `CategoryPrologue`, `CategoryShelfLenses`, `ProductTable`, `ProductRow`, `ExpansionSection`, `ScoreChip`.

### 2.3 Data layer

| Source | Path | Role |
|--------|------|------|
| Primary curated dataset | `src/data/bread-retail-curated.json` | 256 scanned meta; clusters; `all_products`; used by `bread-page-data.ts` |
| Legacy synthetic set | `src/data/bread-comparison.json` | 20 products, BSIP-style fields (`gss`, `ferm_q`, `delta`) — **not** wired to dashboard |

Loader: `src/lib/comparisons/bread-page-data.ts`  
Types: `src/lib/comparisons/bread-types.ts` (`BreadProduct`, clusters, article blocks)

**Product shape (dashboard):** `BreadProduct` with `name_he`, `score`, `grade`, `fiber_g`, `protein_g`, `sodium_mg`, `fermentation_status_he`, `structural_summary_he`, `why_featured_he`, `confidence_label_he`, `image_url`, `source_url`, cluster metadata — **not** `BariProductVM`.

### 2.4 Filters (today)

- **Model:** `BreadFilterId` — single active filter (`all` | cluster ids).
- **Logic:** `breadProductMatchesFilter` in `bread-page-data.ts` (cluster membership).
- **UI:** Custom pill styling inside dashboard (green active state), not `CategoryShelfLenses`.

Reference template uses **multi-select AND lenses** with ids like `less-sweet`. Bread cluster filters are **semantically different** and must be re-authored as category-owned shelf lenses (labels + match rules in `{category}-shelf-filters.ts`), not copied as-is into shared components.

### 2.5 Visual and IA deltas vs frozen template

| Area | Bread today | Reference v1 (מעדנים) |
|------|-------------|------------------------|
| Layout | Full-width `HomeContainer`, desktop table | 375px phone frame, single column |
| Hero | Large investigative hero + stats | `CategoryHero` (eyebrow, title, metadata line) |
| Intro | Inline in hero paragraphs | `CategoryPrologue` (2–3 sentences) |
| Product list | Sortable table rows, 6 columns visible | Zebra `ProductRow` + expand `ExpansionSection` |
| Expansion | Inline table cells (fiber, fermentation, structure) | v2 interpretive blocks + technical block below hairline |
| Extra sections | Insights, pairs, transparency archive | **Forbidden** on comparison route per reference |
| Methodology | `<details>` accordion | `MethodologyFooter` (static lines) |
| Images | `BreadShelfProductImage` / mark fallback; most `image_url` empty | `ProductRow` Next `Image` |
| Score display | `formatBreadScoreLine` + `breadScoreObservation` | `ScoreChip` only in row header |
| Client sort | None on table (filter only) | No sort (corpus order) — aligned once migrated |

### 2.6 Coupling and dependencies

- Blog articles import `bread-page-data` / `bread-types` (`bread-analysis-content.ts`, editorial blocks).
- `FeaturedBreadIntelligenceCardLite` on `/hashvaot` points to `/compare/bread-comparison`.
- Bread-specific components: `bread-shelf-product-image.tsx`, `bread-confidence-pill.tsx` — overlap with `ExpansionSection` confidence footer and `ScoreChip`.

---

## 3. Target architecture

```text
/hashvaot/bread                    (canonical production route)
  → page.tsx                       (metadata + static props OR registry factory)
  → ComparisonShelfPage            (or thin BreadComparisonPage wrapper)
      → CategoryHero
      → CategoryPrologue
      → CategoryShelfLenses        (bread-shelf-filters.ts)
      → ProductTable → ProductRow → ExpansionSection
      → MethodologyFooter

Data:
  src/data/comparisons/bread_frontend_v2.json
  src/lib/comparisons/bread-page-data.ts      (load via corpus.ts)
  src/lib/comparisons/bread-shelf-filters.ts
  src/lib/comparisons/registry/categories/bread.ts
```

**Registry:** Register `bread` in `ComparisonCategoryId` after corpus and adapter exist.

**Blog:** Keep `bread-page-data` exports needed for articles; comparison route consumes **only** `BariProductVM[]` from v2 corpus.

---

## 4. Required adapters

### 4.1 `BreadProduct` → `BariProductVM`

| Bread field | BariProductVM field | Notes |
|-------------|---------------------|-------|
| `id` | `id` | Stable `product_id` |
| `name_he` | `name` | Verbatim |
| `image_url` | `imageUrl` | Often `null`; need corpus-level image policy (placeholder vs omit) |
| `score` | `score` | Integer rounding policy must match מעadנים (corpus pre-rounded) |
| `grade` | `grade` | `BreadGrade` ⊆ `BariGrade` |
| `why_featured_he` or `structural_summary_he` | `insightLine` | **Content decision:** one pre-authored line for collapsed row |
| `confidence_level` | `confidence` | Map `full`→`verified`, `partial`→`partial`, `missing`/`insufficient`→`insufficient` |
| N/A | `expansion` | **Must be built in corpus export**, not inferred at runtime from `ferm_q`/GSS |

### 4.2 Expansion (`BariExpansionVM`) — corpus authoring required

Reference order: positive → limiting → bottom line → **הקשר במדף** → technical block.

Bread raw fields that **cannot** appear in UI copy: `gss`, `ferm_q`, `fiber_q`, `delta`, `degradation_level`, internal cluster ids.

**Proposed mapping sources (authoring, not runtime):**

| v2 field | Bread source (human rewrite) |
|----------|------------------------------|
| `positiveSignals[]` | Strengths from `structural_summary_he`, fermentation positives |
| `limitingFactors[]` | Limits without cap/score language |
| `bottomLine` | `why_featured_he` or synthesized editorial line |
| `comparisonContext` | Shelf-relative sentence (no algorithm terms) |
| `nutrition` | `fiber_g`, `protein_g`, `sodium_mg`, energy if available — per 100g |
| `ingredients` | Full ingredients string if available in corpus |
| `confidenceLabel` | Pre-authored Hebrew (may override shared footer mapping) |
| `servingNote` | e.g. `ל-100 גרם` |

### 4.3 Page copy adapter

| Reference field | Bread source |
|-----------------|--------------|
| `hero.eyebrow` | e.g. `לחם` (not `BREAD INVESTIGATION`) |
| `hero.title` | Editorial title aligned with reference tone |
| `metadataLine` | `formatComparisonMetadataLine(count, generated)` from `_meta` |
| `prologueSentences` | 2–3 sentences from current hero/deck (trim stats-heavy copy) |
| `methodologyLines` | Extract from current `<details>` methodology (split into lines) |

### 4.4 Shelf filters adapter

Replace cluster **single-select** with reference **multi-select AND** lenses only if product rules can be expressed without cluster ids in UI.

Options:

1. **Re-author lenses** (recommended): e.g. `short-ingredient-list`, `high-fiber`, `true-sourdough` with thresholds on `BariProductVM.expansion` / nutrition — parallel to `maadanim-shelf-filters.ts`.
2. **Temporary cluster lenses:** Map cluster membership to lens ids; document as v1 bread-only until `BariCategoryPageVM.filters` exists.

Do **not** port dashboard filter styling into `CategoryShelfLenses`.

### 4.5 Products not on the shelf

Bread features **31 scored** + **transparency (unscored)** products.

Reference rule: corpus order, unscored appended last; row shows `—` chip.

- Include insufficient-data products in JSON with `score: null` **or** exclude from comparison corpus and keep transparency narrative **only on blog**.
- **Decision required:** Reference מעadנים keeps insufficient in list; bread should match unless product explicitly excludes transparency rows.

---

## 5. Required data transformations

### 5.1 New canonical corpus file

**Target:** `src/data/comparisons/bread_frontend_v2.json`

Structure (mirror מעadנים):

```json
{
  "_meta": {
    "generated": "ISO-8601",
    "category": "bread",
    "product_count": N,
    "scored_count": N,
    "version": "v2-production",
    "schema": "BariProductVM[]"
  },
  "products": [ /* BariProductVM + optional _calibration */ ]
}
```

**Build pipeline (out of repo scope for this plan):**

1. Start from `bread-retail-curated.json` scored + displayable products.
2. Apply editorial pass for v2 expansion fields (no runtime generation).
3. Set final shelf order in JSON (score desc, insufficient last).
4. Strip `_calibration` via `loadComparisonCorpus`.
5. Validate against `comparison_corpus_validation_plan_v1.md` before merge.

### 5.2 Loader module pattern

Refactor `bread-page-data.ts` to:

- Import v2 JSON only for **comparison route** payload.
- Keep legacy `BreadProduct` exports for **blog** until articles migrate (or isolate `bread-blog-data.ts`).

### 5.3 Image integrity

- Curated bread: many `image_url` values empty; dashboard uses `BreadShelfProductImage` mark.
- `ProductRow` expects real URLs or broken image handling — define corpus rule: nullable `imageUrl` + existing row fallback behavior.
- Confirm `next.config.ts` remote patterns for any new hosts (Shufersal cloudinary already allowed).

---

## 6. Migration path (phased)

### Phase 0 — Decisions (blocking)

| Decision | Owner | Default recommendation |
|----------|--------|-------------------------|
| Canonical slug | Product | `/hashvaot/bread` (English slug matches `maadanim` pattern) or `/hashvaot/lechem` (Hebrew) — pick one, never both live |
| Transparency rows on shelf | Editorial | Include as `score: null` rows at corpus tail |
| Dashboard-only sections | Editorial | Move insight blocks + pairs to blog; do not add to `ComparisonShelfPage` |
| Corpus authoring | Content/audit | New v2 JSON; no adapter-only migration from raw curated JSON |

### Phase 1 — Corpus + validation (no UI)

1. Produce `bread_frontend_v2.json`.
2. Run validation plan (CI script later).
3. Add `bread-page-data.ts` loader using `corpus.ts` (mirror `maadanim-page-data.ts`).

### Phase 2 — Filters + registry (no public route switch)

1. Add `bread-shelf-filters.ts`.
2. Register `bread` in `comparisonCategoryRegistry`.
3. Add dev corpus API or extend registry dev path for bread QA.

### Phase 3 — Shelf route behind flag or preview

1. Add `src/app/hashvaot/bread/page.tsx` using `createComparisonCategoryRoute("bread")` or explicit `ComparisonShelfPage` wiring.
2. QA against reference checklist (pixel, expansion order, no sort, 375px frame).
3. Compare product count and order to signed-off corpus.

### Phase 4 — Route cutover

1. Point `BREAD_COMPARISON_HREF` → `/hashvaot/bread`.
2. Redirect `/compare/bread-comparison` → `/hashvaot/bread` (301).
3. Keep `/hashvaot/bread-comparison` redirect chain updated.
4. Update `/hashvaot` featured card href.

### Phase 5 — Retire legacy dashboard

1. Mark `BreadComparisonDashboard` deprecated; remove from production route.
2. Quarantine or delete after link audit: dashboard-only components if unused by blog.
3. Document retirement in changelog.

**Estimated engineering sequence:** Phase 0 → 1 → 2 → 3 (QA) → 4 → 5.  
**Do not** flip production redirects before Phase 3 QA sign-off.

---

## 7. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **IA regression** — users expect dashboard table, pairs, transparency grid | HIGH | Explicit comms; blog retains deep editorial; comparison route is shelf-only by design |
| **Content loss** — fermentation/fiber columns hidden inside expansion | HIGH | Author v2 expansion + nutrition grid; editorial review per product |
| **Image gaps** — null URLs across bread corpus | HIGH | Corpus image pass or acceptable `ProductRow` fallback; document in QA |
| **Filter semantics change** — cluster single-select → AND lenses | MEDIUM | Re-author filters with product team; document mapping |
| **Blog breakage** — shared `bread-page-data` refactor | MEDIUM | Split comparison vs blog data modules early |
| **Dual routes during migration** | MEDIUM | Short redirect matrix; avoid three live URLs |
| **Confidence label drift** — `ExpansionSection` maps `BariConfidence` to fixed Hebrew | LOW | Prefer `expansion.confidenceLabel` from corpus where authored |
| **Fiber not in shared nutrition grid** | MEDIUM | Accept for v1 parity with מעadנים or schedule shared component change (separate design pass) |

---

## 8. Out of scope (this migration)

- Milk comparison (`milk-comparison-page.tsx`) — separate program.
- Scoring methodology or BSIP pipeline changes.
- New comparison UI sections, search, maps, pair cards on shelf route.
- `bread-comparison.json` synthetic demo data — retire or keep dev-only.

---

## 9. Acceptance criteria (bread on reference template)

- [ ] `/hashvaot/bread` renders `ComparisonShelfPage` stack only.
- [ ] Products are `BariProductVM[]` from `bread_frontend_v2.json`.
- [ ] No client-side re-sort in `ProductTable`.
- [ ] Expansion labels match reference (`הקשר במדף`, etc.).
- [ ] No BSIP/NOVA/caps/dimension language in user-facing strings.
- [ ] Legacy `/compare/bread-comparison` redirects to canonical route.
- [ ] `bread` registered in comparison registry.
- [ ] `npm run lint` + `npm run build` pass.
- [ ] QA script or checklist run against production route (not only `/dev/preview`).

---

## 10. Files touched (implementation preview)

| Action | Path |
|--------|------|
| Create | `src/data/comparisons/bread_frontend_v2.json` |
| Create | `src/lib/comparisons/bread-shelf-filters.ts` |
| Create | `src/lib/comparisons/registry/categories/bread.ts` |
| Refactor | `src/lib/comparisons/bread-page-data.ts` |
| Create | `src/app/hashvaot/bread/page.tsx` |
| Redirect | `src/app/compare/bread-comparison/page.tsx` |
| Update | `src/lib/blog/bread-analysis-content.ts` (`BREAD_COMPARISON_HREF`) |
| Retire | `src/components/comparisons/bread-comparison-dashboard.tsx` (post-cutover) |
