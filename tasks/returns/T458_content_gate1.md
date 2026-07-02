# TASK-458 — Content Agent gate 1 return (catalog go-live)

**Task:** TASK-458 (Content sign-off, gate 1 of 2)
**Branch:** `golive/catalog-task458` (worktree `C:\bari_wt_t458`)
**Commit (this pass):** `4cf7dc3e` — "TASK-458 gate 1: catalog copy honesty + voice pass"
**Proposed status:** RETURNED (awaiting Adversarial QA / Red-Team, gate 2)

## Scope discipline

Strings/copy only. No logic, layout, schema, or data changes. Two files touched:
`bari-web/src/app/catalog/page.tsx`, `bari-web/src/components/inventory/product-table.tsx`.

## Coverage fact-check (why the honesty fix was needed)

- `bari-web/src/lib/comparisons/registry/index.ts` registers exactly **7** categories in
  `comparisonCategoryRegistry`: bread, snacks, hummus, cheese, breakfast-cereals, granola,
  crackers.
- `bari-web/src/app/hashvaot/` has **21** route folders live (bread, breakfast-cereals,
  brined-cheeses, cakes, cheese, chocolate-bars, chocolate-tablets, cookies-coffee, crackers,
  granola, hard-cheeses, hummus, juices, magnesium, milk-comparison, personal-care,
  protein-bars, raw-foods, snacks, supermarket, supplements) — milk, magnesium, chocolate,
  juices and 10 others are live at `/hashvaot` but absent from `/catalog`.
- 209 products, per the P458 return's registry-corpus count. Confirms the brief: a search for
  "חלב" on `/catalog` returns zero rows under a page that (pre-fix) claimed "כל המוצרים."

## Full string inventory (verbatim, file:line) — verdict per string

### `bari-web/src/app/catalog/page.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 1 | page.tsx:36 | `קטלוג המוצרים \| Bari` (metadata.title) | **Kept, approved.** Neutral label, no overreach. |
| 2 | page.tsx:37 | `כל המוצרים שבארי בדקה — מדורגים לפי קטגוריה, רשת ואיכות תזונתית.` (metadata.description) | **CHANGED.** Dishonest — claims "all products" while 7/21+ categories are covered. This is the SEO/share description; it needed the same honesty fix as the on-page copy. |

New description (page.tsx:37-38): `המוצרים שבארי כבר בדקה, מדורגים לפי קטגוריה, רשת ואיכות תזונתית. הקטלוג גדל כל שבוע.`
Rationale: "המוצרים שבארי כבר בדקה" (the products Bari has already checked) truthfully scopes the set as a subset, not "all." "הקטלוג גדל כל שבוע" (the catalog grows every week) reframes the gap as a work-in-progress instead of a hidden limitation — matches the page's own live subtitle ("עודכן השבוע"). No em dash, no health claim, no puffery.

### `bari-web/src/app/catalog/_catalog-client.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 3 | :113 | `קטגוריות` (sidebar section label) | Kept, approved. |
| 4 | :157 | `כל הקטגוריות` (sidebar "all" button) | Kept, approved. |
| 5 | :196 | `{cat.nameHe}` (dynamic, from registry) | Kept — data-driven, not authored copy. |
| 6 | :226 | `ניווט` (sidebar nav section label) | Kept, approved. |
| 7 | :241 | `השוואות` (sidebar link label) | Kept, approved. |
| 8 | :242 | `בלוג` (sidebar link label) | Kept, approved. |
| 9 | :243 | `מדדים ושיטה` (sidebar link label) | Kept, approved. |
| 10 | :305 | `הכל` (mobile category strip "all" pill) | Kept, approved. |
| 11 | :369 | `BARI CATALOG` (eyebrow label) | Kept, approved — brand mark, not a coverage claim. |
| 12 | :375 | `קטלוג המוצרים` (H1) | Kept, approved. Neutral; does not claim completeness. |
| 13 | :378-380 | `{totalProducts} מוצרים · {categoryCount} קטגוריות פעילות · עודכן השבוע` (dynamic subtitle) | **Kept, approved — already honest.** States real counts (209 / 7) computed from `summary`, not a "complete" claim. This is the correct honest-scoping pattern; the fix in `page.tsx` metadata brings the `<meta>` description in line with what this on-page line already does correctly. |
| 14 | :428 | `כל המוצרים` (product table card heading) | Kept, approved — "all [of the filtered] products," standard table-heading idiom in context of a product table, not a coverage claim about the whole product universe. Sits directly above a table whose row count and filters are visible, so the local meaning is unambiguous. |
| 15 | :441 | `נקה סינון ×` (clear filter button) | Kept, approved. |
| 16 | :404-416 (card headings) | `פילוח לפי ציון`, `קטגוריות מובילות` | Kept, approved. |
| 17 | :80 | `ניווט קטלוג` (aria-label) | Kept, approved. |
| 18 | :118 | `קטגוריות מוצרים` (aria-label) | Kept, approved. |
| 19 | :238 | `קישורי אתר` (aria-label) | Kept, approved. |
| 20 | :287 | `סינון לפי קטגוריה` (aria-label, mobile strip) | Kept, approved. |

### `bari-web/src/components/inventory/product-table.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 21 | :287 | `חיפוש שם מוצר, מותג...` (search placeholder) | Kept, approved. |
| 22 | :290 | `חיפוש מוצר` (aria-label) | Kept, approved. |
| 23 | :298 | `סינון מוצרים` (aria-label, filter bar) | Kept, approved. |
| 24 | :300 | `כל הקטגוריות` (select option) | Kept, approved. |
| 25 | :298,311 | `סינון לפי קטגוריה`, `סינון לפי רשת` (aria-labels) | Kept, approved. |
| 26 | :312 | `כל הרשתות` (select option) | Kept, approved. |
| 27 | :91-97 | Grade filter options: `כל הדרגות`, `A`..`E`, `ללא ציון` | Kept, approved. |
| 28 | :82-86 | Column labels: `מוצר`, `קטגוריה`, `ציון`, `רשת` | Kept, approved. |
| 29 | :689 | `רשת · מקור` (desktop column header) | Kept, approved. |
| 30 | :357 | `מיין לפי {label}` (aria-label template) | Kept, approved. |
| 31 | :589 | `{filtered.length} מוצרים מוצגים` (results count, dynamic + honest) | Kept, approved. |
| 32 | :596 | `מיין לפי` (mobile sort label) | Kept, approved. |
| 33 | :609 | `ברירת מחדל` (sort select default option) | Kept, approved. |
| 34 | :618 | `מיון עולה` / `מיון יורד` (aria-labels) | Kept, approved. |
| 35 | :672 | `טבלת מוצרים` (table aria-label) | Kept, approved. |
| 36 | :692 | `צפייה ברשת` (sr-only column header) | Kept, approved. |
| 37 | :698 | `פרטים` (sr-only column header, expansion) | Kept, approved. |
| 38 | :227 | `צפייה במוצר באתר הרשת` (buy-affordance title, active) | Kept, approved. |
| 39 | :236 | `צפייה ברשת` (buy-affordance link text, active) | Kept, approved. |
| 40 | :247 | `בקרוב — צפייה במוצר באתר הרשת` (buy-affordance title, dormant) | Kept, approved — accurately signals "coming soon," not a live claim. |
| 41 | :256-257 | `צפייה ברשת`, `· בקרוב` (buy-affordance dormant text) | Kept, approved. |
| 42 | :205 | `מותג: {brand}` (aria-label template, dynamic) | Kept — data-driven. |
| 43 | :751 | `הקודם` (pagination) | Kept, approved. |
| 44 | :754 | `עמוד {n} מתוך {total}` (pagination, dynamic) | Kept, approved. |
| 45 | :761 | `הבא` (pagination) | Kept, approved. |
| 46 | :744 | `עימוד` (pagination aria-label) | Kept, approved. |
| 47 | :902,1046 | `סגור פרטים עבור {name}` / `הצג פרטים עבור {name}` (expand aria-labels, dynamic) | Kept, approved. |
| 48 | :1108 (was) | `אין מוצרים בסינון הזה` (EmptyState heading) | **CHANGED.** "No products in this filter" implicitly blames the user's filter choice even when the true cause is coverage (product/category not yet scored). This is the string a first-time visitor hits searching "חלב." |
| 49 | :1111 (was) | `נסו לשנות את פרמטרי הסינון` (EmptyState body) | **CHANGED.** Dead-ends the user with no path forward and no acknowledgment that the catalog is partial. |
| 50 | :1120 | `נסה שוב` (ErrorState retry button) | Kept, approved — unrelated to coverage; generic network/load error retry. |

New EmptyState (product-table.tsx:1104-1124):
- Heading: `לא נמצאו מוצרים תואמים` ("no matching products found" — neutral, doesn't presuppose a filter mistake)
- Body: `נסו לשנות את הסינון, או שהמוצר עדיין לא נבדק. הקטלוג גדל כל שבוע, וכל ההשוואות המלאות נמצאות ב [השוואות→/hashvaot].`
  ("Try changing the filter, or the product hasn't been checked yet. The catalog grows every week, and all full comparisons are at [Comparisons]." — links to `/hashvaot`.)

Rationale: this is the single highest-priority fix per the task brief — it is the honest-empty-state a user searching for an uncovered product (milk, magnesium, etc.) actually sees. It (a) states plainly that absence may mean "not yet checked," not "doesn't exist," (b) reframes it as an active, growing effort rather than a gap, (c) gives a concrete next step to the fuller `/hashvaot` comparison set instead of a dead end. No em dash (uses periods/commas). No "X, not Y" phrasing. No health claim.

### `bari-web/src/components/inventory/inventory-grade-chip.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 51 | :28 | `לא נוקד` (aria-label, unscored chip) | Kept, approved. |
| 52 | :42 | `—` (visible glyph, unscored chip) | Kept, approved. |
| 53 | :51 | `דרגה {grade}` (aria-label template, dynamic) | Kept, approved. |

### `bari-web/src/components/inventory/retailer-donut.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 54 | :104 | `אין נתונים` ("no data" — DonutChart zero-state) | Kept, approved. Fires only if `summary` arrives empty (data-shape guard), not a normal user-reachable path on a live 209-product catalog. Neutral technical fallback. |
| 55 | :93 | `מוצרים` (donut centre sub-label, default) | Kept, approved. |
| 56 | GradeDonut :215 | `ללא ציון` (segment label, dynamic-conditional) | Kept, approved. |
| 57 | GradeDonut :215 | `ציון {grade}` (segment label template) | Kept, approved. |
| 58 | GradeDonut :230 | `פילוח לפי ציון: ...` (aria-label template) | Kept, approved. |
| 59 | RetailerDonut :264 | `פילוח לפי רשת: ...` (aria-label template, unused by catalog per current wiring but present in file) | Kept, approved. |

### `bari-web/src/components/inventory/top-categories-card.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 60 | :95 | `אין קטגוריות.` ("no categories" — zero-state) | Kept, approved. Same reasoning as #54 — unreachable on a live catalog with 7 registered categories; neutral technical fallback, not consumer-facing messaging about coverage. |
| 61 | :104 | `קטגוריות מובילות` (aria-label, list) | Kept, approved. |

### `bari-web/src/components/site-header.tsx`

| # | File:line | String (verbatim) | Verdict |
|---|---|---|---|
| 62 | :22 | `קטלוג` (nav link label) | Kept, approved. Short, neutral, matches sibling labels `השוואות`/`בלוג`/`מדריכים` — no coverage claim in a 2-word nav label. |
| 63 | :36 | `בית Bari` (logo aria-label) | Kept, approved — unrelated to catalog. |
| 64 | :42 | `ניווט ראשי` (nav aria-label) | Kept, approved. |
| 65 | :59,100 | `הרשמו לניוזלטר` (newsletter CTA) | Kept, approved — unrelated to catalog. |
| 66 | :73 | `פתיחת תפריט` (mobile menu button aria-label) | Kept, approved. |
| 67 | :85 | `ניווט נייד` (mobile nav aria-label) | Kept, approved. |

## OG-strings finding (commit `bd1e3a80`)

Reviewed `bari-web/src/lib/seo/open-graph.ts` (new file, `blogOpenGraph()` / `comparisonOpenGraph()` /
`withComparisonOpenGraph()`) plus every blog and `/hashvaot` page.tsx / page-data.ts touched by
`bd1e3a80`, diffed line-by-line against the pre-commit version.

**Finding: clean.** No new copy was authored in this commit. Every changed site:
- Blog pages: pass the *same* `seoMeta.ogTitle` / `seoMeta.ogDescription` (already-existing,
  pre-approved strings from each blog's own `-article-content.ts`) into the new `blogOpenGraph()`
  helper — only the default OG image (`/bari-logo-optimized.webp`, matches root layout default)
  was added, not text.
- `/hashvaot/*` pages: either (a) wrap the pre-existing inline `title`/`description` literal in
  `withComparisonOpenGraph({...})` with the string byte-identical (verified for cakes, magnesium,
  juices-page-data.ts, bread-comparison-page-data.ts, milk-page-data.ts), or (b) switch from an
  inline metadata object to importing the page's own already-exported `*ComparisonMetadata` const
  (verified for juices/page.tsx, hard-cheeses/page.tsx — same string, now single-sourced instead
  of duplicated).
- No health-outcome claims, no puffery, no fabricated copy anywhere in the diff.

No action needed; nothing to replace or re-author. `bari-web/src/lib/seo/open-graph.ts` itself
contains zero Hebrew strings — it's pure plumbing (types + a shared default image constant).

## Hebrew quality check

- RTL: all Hebrew strings render inside `dir="rtl"` containers (page-level and component-level);
  the one Hebrew/English mixed string (`BARI CATALOG` eyebrow, `SKU {row.sku}` label) uses Latin
  tokens as isolated uppercase/mono labels, not inline-mixed prose — no bidi break risk.
  Numeric+Hebrew mixed strings (counts, "עמוד 1 מתוך 3") use `.toLocaleString("he-IL")` and render
  correctly RTL since Hebrew punctuation/spacing around digits is standard practice already used
  site-wide.
- No niqqud anywhere in the surface (confirmed by inspection of all strings above).
- No translationese detected — phrasing throughout ("נסו לשנות," "לא נמצאו מוצרים תואמים," "הקטלוג
  גדל כל שבוע") reads as native Hebrew UI copy, consistent with the site's existing microcopy
  register (e.g. `אין מוצרים בסינון הזה` was itself native-sounding; the fix keeps the same
  register while fixing the honesty problem).
- No "X, not Y" phrasing introduced. Em dashes minimized — the two changed strings use periods
  and commas, not em dashes (the removed metadata description had used one).

## Self-check results

| Command | Exit code |
|---|---|
| `npx tsc --noEmit` (bari-web/) | 0 |
| `npm run build` (bari-web/) | 0 — `/catalog` built as `ƒ /catalog` (dynamic route), no errors |

## Commit

`4cf7dc3e` — "TASK-458 gate 1: catalog copy honesty + voice pass" (2 files changed, 13
insertions, 3 deletions: `bari-web/src/app/catalog/page.tsx`,
`bari-web/src/components/inventory/product-table.tsx`)

## Summary counts

- **Strings inventoried:** 67
- **Strings changed:** 3 (metadata description; EmptyState heading; EmptyState body)
- **Strings kept, approved:** 64
- **OG-authored-copy findings:** 0 (clean — refactor only, verified line-by-line)

---

```json
{
  "task": "TASK-458",
  "gate": 1,
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/src/app/catalog/page.tsx",
      "action": "modified",
      "change": "metadata.description honesty fix"
    },
    {
      "path": "bari-web/src/components/inventory/product-table.tsx",
      "action": "modified",
      "change": "EmptyState heading + body honesty fix, links to /hashvaot"
    },
    {
      "path": "tasks/returns/T458_content_gate1.md",
      "action": "created",
      "change": "full string inventory + verdicts + OG finding"
    }
  ],
  "counts": {
    "strings_inventoried": 67,
    "strings_changed": 3,
    "strings_kept_approved": 64,
    "og_new_copy_findings": 0
  },
  "commands_run": [
    { "cmd": "npx tsc --noEmit (bari-web/)", "exit_code": 0 },
    { "cmd": "npm run build (bari-web/)", "exit_code": 0 }
  ],
  "not_done": [
    "Adversarial QA / Red-Team sign-off (gate 2)",
    "push/PR/deploy"
  ],
  "self_check": "npx tsc --noEmit exit 0 and npm run build exit 0 in the worktree after all copy edits, observed directly.",
  "commit_sha": "4cf7dc3e"
}
```
