# Derived Views Scoping v1 — TASK-568

Owner: Frontend Agent. Scope: `bari-web/src/components/hashvaot/featured-*-intelligence-card.tsx`
(~18 files present; task summary said "~16"). Goal: replace hand-maintained
score/grade/count literals with build-time derivation from the same comparison JSON the
actual category page reads, without touching approved copy.

## 0. Load-bearing discovery: the "תובנות מרכזיות" prop is dead code

`ComparisonIntelligenceHero` (`src/components/comparisons/comparison-intelligence-hero.tsx:31-34`)
marks `insightLines` and `showInsights` `@deprecated — Removed 2026-07-01 — insights section
deleted. Prop accepted but ignored.` Every card still constructs an `INSIGHT_LINES` array
(hardcoded, or `product.insightLine` mapped with a hardcoded fallback) and passes it in —
**none of it renders.** This cuts real scope: per-product insight-line derivation is not
needed for the visible surface. Confirmed by reading the component body (lines 46-210): only
`badge`, `categoryTags`, `title`, `description`, `stats[]`, and `updatedLabel` reach the DOM.

## 1. Per-card audit (6 cards read: cheese, protein-bars, juices, breakfast-cereals, granola,
magnesium — chosen for spread: JSON-driven clean cards, JSON-driven cards with extra
hand-typed stats, and one structurally-different hand-authored card)

| Card | Field | Classification | Current source | Drift finding |
|---|---|---|---|---|
| cheese | `stats: productCount, scoredCount, aGradeCount` | **data** | `cheeseProducts.filter(...)` inline, JSON-backed | none — already correct, good pilot baseline |
| cheese | `insightLines` (4 lines) | dead code | hardcoded array | not rendered, out of scope |
| cheese | `title`, `description`, `badge`, `categoryTags` | **copy** | `getComparisonPageChrome`, prop, literal | leave as-is |
| cheese | `theme.photo` | **design** | stock category image `/hashvaot/themes/cheese.jpg` | stock-image rule respected, leave |
| protein-bars | `stats[0]` productCount | **data** | `.length`, JSON-backed | none |
| protein-bars | `stats[1]` `"25–34"` grams/100g | **data, hardcoded literal** | typed string | **DRIFT: actual JSON min/max protein is 25–36, not 25–34** (verified via `protein_combined_frontend_v2.json`) |
| protein-bars | `stats[2]` `"B"` "תקרת הקטגוריה" (category ceiling) | **data, hardcoded literal** | typed string | currently accurate (grades present: B/C/D, no A) but fragile — will silently go stale on next re-score |
| juices | `stats: productCount, scoredCount, aCount` | **data** | inline filters, JSON-backed | none |
| breakfast-cereals | `stats[0]` productCount | **data** | `.length`, JSON-backed | none |
| breakfast-cereals | `stats[1]` `38` "פרמטרים הושוו" (params compared) | **data, hardcoded literal** | literal number | **not derivable from this JSON** — no per-product or meta field counts "parameters compared." Needs a Data Agent-owned methodology constant in JSON `_meta`, or removal. Not fixed in this pilot. |
| breakfast-cereals | `stats[2]` `4` "קטגוריות" | **data, hardcoded literal** | literal number | same as above — not derivable from product-level JSON, flagged not fixed |
| granola | `stats[0]` productCount | **data** | `.length`, JSON-backed | none |
| granola | `stats[1]` `38` "פרמטרים הושוו" | **data, hardcoded literal** | literal number | same non-derivable-constant issue as cereals |
| granola | `stats[2]` `47` "נקודות פער" (score-gap points) | **data, hardcoded literal** | literal number | **DRIFT: actual JSON score spread (max−min) is 38.3 → 38, not 47** (verified: `granola_frontend_v2.json` scores range 31.4–69.7). This is exactly the TASK-519-class drift the task targets. |
| granola | (companion) `supermarket/page.tsx:77` `granolaDescription` prose | **copy**, contains the same stale "47" | inline template string, two-gate content | **NOT touched** — this is prose (editorial paragraph), not a card stat; flagging for Content Agent, out of my mandate per the copy carve-out |
| magnesium | `stats: productCount, bCount, cCount, dCount` | **data** | inline filters over `magnesiumProducts` | none currently, but... |
| magnesium | `updatedLabel="עודכן יוני 2026"` | **data, hardcoded literal** | literal string, NOT derived | **structural gap, not just a card bug**: `magnesium-page-data.ts` is a fully hand-authored TS literal array with **no raw JSON import and no `corpusMeta.generated` field at all** — it does not use `loadComparisonCorpus`, unlike every other category (violates the "uniform baseline" pattern the rest of the site follows). There is nothing to derive `updatedLabel` from without Data Agent first adding a `generated` date to a real magnesium JSON export. **Excluded from this pilot** — flagging as a separate, larger finding (see §4). |
| all cards | `theme.photo` | **design** | stock category image per stock-image rule | never product photos on `/hashvaot` cards — respected everywhere audited |

## 2. Leader/runner-up names

None of the 16 hashvaot featured cards render a leader/runner-up product name today (the task
summary's mention of "leader names" does not match current card output — `insightLines` is the
closest thing and it's dead code, see §0). The derived shape below still reserves an optional
leader field so a future card can add it without a second derivation layer, but nothing is wired
to it in this pilot.

## 3. Prior art already doing exactly this pattern (build on it, don't reinvent)

`src/lib/home/homepage-carousel-category-stats.ts` already derives grade distributions and
sugar-mask stats straight from raw JSON at build time (`deriveGradeDistribution`,
`CEREALS_SUGAR_MASK_STATS`) for the **homepage carousel**, and `src/lib/home/featured-cereal-duel.ts`
derives a two-product duel (score/grade/sugar/fiber) by product-ID lookup into raw JSON
(`getFeaturedCerealDuel`). Both are the same "derive from JSON, never hand-type" pattern TASK-568
asks for — just not yet applied to the `/hashvaot` cards, and not shared as a common module.

**Sibling drift risk found, out of this task's stated scope but same failure class:**
`src/lib/home/homepage-carousel-data.ts` (`HOMEPAGE_CAROUSEL_CARDS`) is fully hand-typed —
`leftProduct.score: 89`, `rightProduct.score: 60`, names, brands, and an `evidence` string
embedding "פער של כ-29 נקודות" are all literals, unverified against `bread_frontend_*.json`.
This is the "homepage carousel" the task title references. I did not touch it — the delegation's
Phase 2 explicitly scopes to the `hashvaot/featured-*-intelligence-card.tsx` files. Recommend a
follow-up task once the pilot module is proven, reusing the same `deriveComparisonCardStats`
module against `HOMEPAGE_CAROUSEL_CARDS`' product IDs.

## 4. The derived data shape + module location/API

New file: **`src/lib/derived/comparison-card-stats.ts`**. Pure functions, no React, no `"use client"`.

Deliberately typed against a minimal structural shape (`{ score, grade }`) rather than the full
`BariProductVM`, so the exact same function runs against (a) the already-loaded `BariProductVM[]`
a card imports, and (b) a raw-JSON-parsed product array in the parity script — true apples-to-apples
comparison, no duplicated logic path.

```ts
export type CardGradeLetter = "A" | "B" | "C" | "D" | "E";

export interface CardStatsProductInput {
  score: number | null;
  grade: CardGradeLetter | null;
}

export interface ComparisonCardStats {
  productCount: number;
  scoredCount: number;
  gradeCounts: Record<CardGradeLetter, number>;
  /** Best (lowest-letter) grade actually present among scored products, or null if none scored. */
  ceilingGrade: CardGradeLetter | null;
  scoreLow: number | null;
  scoreHigh: number | null;
  /** Rounded to a whole point — "UI never rounds" per view-model doctrine, so the
   *  derivation layer owns the rounding, not the JSX. */
  scoreSpread: number | null;
  updatedLabel: string;
}

export function deriveComparisonCardStats(
  products: readonly CardStatsProductInput[],
  generatedAt: string
): ComparisonCardStats;

/** Generic min/max helper for a single numeric metric (e.g. protein g/100g). */
export function deriveMetricRange(
  values: readonly (number | null | undefined)[]
): { low: number; high: number } | null;
```

Internal dependency: `formatComparisonUpdatedLine` from `../comparisons/format-comparison-updated-line`
(relative import — that file has zero imports of its own, so this stays importable both from
Next/webpack via the card components and from plain `node` in the parity script; see §5).
`BariProductVM`/`BariGrade` types are imported `import type { ... } from "@/lib/view-models"` —
type-only imports are erased by Node's native TS stripping (verified empirically: a `@/`-aliased
`import type` runs fine under plain `node <file>.ts` on Node 24; a *value* import from `@/...`
does not resolve and would break the parity script). This constrains the module to relative-only
value imports — documented as a comment at the top of the file so a future edit doesn't
accidentally add an aliased value import and silently break the parity gate.

Cards call it as: `const stats = deriveComparisonCardStats(xProducts, xCorpusMeta.generated);`
then read `stats.productCount`, `stats.scoredCount`, `stats.gradeCounts.A`, `stats.ceilingGrade`,
`stats.scoreSpread`, `stats.updatedLabel` in place of their own inline filters/literals.

## 5. Parity-check design (CI fixture)

No vitest in this repo (checked `package.json` — Playwright + a plain `node scripts/*.mjs`
gate, `validate-corpus.mjs`, is the existing convention for a non-browser data gate). Matching
that convention rather than adding a test-runner dependency:

**New file: `scripts/validate-card-stats.mjs`** (or `.ts` — Node 24 runs `.ts` directly via
native type-stripping, confirmed by a scratch test in this session; no `tsx`/`ts-node` needed).

For each pilot category manifest entry `{ id, jsonPath }`:
1. `fs.readFileSync(jsonPath)` + `JSON.parse` — reads the raw frontend JSON directly, same as
   `validate-corpus.mjs` does, so it needs no path-alias resolution for the JSON itself.
2. Calls `deriveComparisonCardStats(raw.products, raw._meta.generated)` — imported via a
   **relative** path (`../src/lib/derived/comparison-card-stats.ts`), which plain `node` can
   load directly (relative imports always resolve; the module's only `@/` imports are
   type-only and erase to nothing, per §4).
3. Prints the derived `ComparisonCardStats` and exits 0. (This pilot version establishes the
   fixture shape; a stricter mode that also greps the compiled card `.tsx` source for a literal
   number disagreeing with the derived value is the natural next hardening step, flagged as a
   TODO comment rather than built now — out of pilot scope but the manifest/derive plumbing is
   what makes it possible later.)

Wired as `"validate-card-stats": "node scripts/validate-card-stats.mjs"` in `package.json`
(mirrors `"validate-corpus"`), so it is `npm run`-invocable and can join `barint_ci`'s frontend
job in a follow-up — workflow files are intentionally not touched in this task per the delegation
spec.

## 6. Pilot selection (Phase 2)

Three cards, chosen to cover all three patterns found in §1:

1. **protein-bars** — has a confirmed numeric drift (`"25–34"` → real `25–36`) and a fragile
   hardcoded ceiling grade (`"B"`, currently correct).
2. **granola** — has a confirmed numeric drift (`47` → real `38`) on `scoreSpread`.
3. **cheese** — already-correct baseline (counts computed inline from the JSON-backed array);
   converting it proves the shared module is behavior-preserving where there is no drift, not
   just where there is.

Magnesium is explicitly excluded from the pilot (§1) — it has no JSON `generated` source to
derive `updatedLabel` from; fixing it means first giving it a real corpus export, which is a
Data Agent-scoped follow-up, not a frontend derivation change.

## 7. Addendum — state at implementation time (worktree based on `origin/master`, not `task506`)

§1's audit was read against the local `task506` branch. The TASK-568 worktree is required to
branch from `origin/master` (per the delegation spec), which had moved independently since:
**both confirmed drifts in §1 were already hand-fixed on `origin/master` before this pilot
touched any code** — `protein-bars` already reads `"25–36"` (matching the JSON) and `granola`
already *computes* its score-spread inline (`Math.round(Math.max(...) - Math.min(...))`, giving
37 on the current JSON, not the stale hardcoded `47`) rather than hardcoding it. `breakfast-cereals`
also no longer carries the non-derivable `38`/`4` "params compared"/"categories" stats found in
§1 — it now shows JSON-backed B/D grade counts instead.

This does not make §1's findings wrong — it independently *proves* the failure class: two
different numbers went stale in production-facing cards and had to be manually caught and
hand-edited, twice, with no gate to catch it happening a third time. It does mean the Phase 2
pilot below ships **zero consumer-visible change** — every converted card's displayed stat is
byte-identical before/after, verified by construction (granola's own pre-existing inline
`Math.round(Math.max(...)-Math.min(...))` and cheese/protein-bars' pre-existing
`.filter(...).length` are mathematically identical to what `deriveComparisonCardStats` computes
over the same array). The deliverable is architectural: one shared, build-time module replacing
per-card duplicated (and previously hand-broken) computation — not a live bug fix. See the
TASK-568 return for the exact before/after per pilot card.
