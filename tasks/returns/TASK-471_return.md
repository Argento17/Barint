# TASK-471 Return — Per-product canonical pages /p/[barcode] + OG images + barcode search

Status proposed: **RETURNED** (not CLOSED — orchestrator verifies and closes)

## What was built

### 1. Canonical product page — `/p/[barcode]`
- `C:\Bari\bari-web\src\app\p\[barcode]\page.tsx` (new)
  - Server Component. Looks up the product via `getProductByBarcode(barcode)` (new loader
    function, see below). Unknown barcode → `notFound()` (404), never a fabricated page
    (`dynamicParams = false`).
  - `generateStaticParams()` emits one static path per barcode in the live corpus (SSG,
    `dynamic = "force-static"`).
  - Renders: back-link to the category comparison page, product image (or letter-tile
    fallback), name, brand (with in-name suppression matching the existing catalog logic),
    category (linked), `ScoreChip` (canonical shared component, unmodified), the signed-off
    `rowVerdict` (falling back to `insightLine`) verbatim, the full `ExpansionSection` (via a
    thin client wrapper — see below), and the category's `MethodologyFooter` +
    `NotMedicalAdvice`, both rendered verbatim from the same data the comparison pages use.
  - 100% reuse of canonical components: `ScoreChip`, `ExpansionSection`, `MethodologyFooter`,
    `NotMedicalAdvice`. No new score/grade/nutrition rendering logic was written — every
    value is read as-is off `BariProductVM`. No BSIP/NOVA/pillar/cap/dimension term appears
    in any rendered string.

- `C:\Bari\bari-web\src\app\p\[barcode]\_expansion-client.tsx` (new)
  - Thin `"use client"` wrapper solely so `ExpansionSection`'s `onCollapse` callback (a
    function, which cannot cross the Server→Client props boundary) can be a local no-op.
    Zero data transformation — pure passthrough of the same `BariProductVM` fields the
    catalog page already passes to the same component.

### 2. Per-product OG image
- `C:\Bari\bari-web\src\app\p\[barcode]\opengraph-image.tsx` (new)
  - `next/og` `ImageResponse`, 1200×630, PNG.
  - **DEGRADED per the spec's explicit fallback clause** — see "OG Hebrew rendering" below.
  - Shows: Bari wordmark, the numeric score, the grade letter, and the barcode digits, on
    the grade-color brand template. No product name (Hebrew) is baked into the image.
  - `generateMetadata()` in `page.tsx` wires Hebrew title/description into
    `openGraph`/`twitter` metadata (the *page's* meta tags are full, correct Hebrew — only
    the generated PNG itself is Latin/numeric-only).

### 3. Barcode/name search entry
- `C:\Bari\bari-web\src\lib\inventory\loader.ts` (edited — additive only)
  - Added `BarcodeProductEntry`, `buildBarcodeProductIndex()`, `getProductByBarcode()`.
    Joins `InventoryProductRowVM.sku` (barcode) to the matching `BariProductVM` by shared
    `id`. Products with no barcode are skipped (never fabricated). Existing exports
    (`buildInventoryRows`, `buildInventorySummary`, `buildInventoryProductDetails`)
    untouched.
- `C:\Bari\bari-web\src\components\inventory\product-table.tsx` (edited)
  - Search placeholder now mentions barcode; the search haystack now includes `row.sku` so
    typing a barcode filters the table (not just names/brands).
  - New `exactBarcodeMatch` memo + a green jump banner ("התאמת ברקוד מדויקת: מעבר לעמוד
    המוצר של…") that appears only on an exact `sku` match, linking to `/p/[barcode]`.
  - New `ProductPageLink` component: every public-catalog row (desktop + mobile) with a
    barcode gets a small "עמוד מוצר ←" link to its `/p/[barcode]` page, alongside the
    existing name→category-comparison link. Admin variant unchanged (no `sku` link there —
    admin already shows SKU as plain text).
  - No changes to filtering/sorting logic beyond adding `sku` to the search haystack; sticky
    header, KPI strip, and existing columns are untouched.

## New Hebrew UI strings introduced (for the orchestrator's two-gate)

All of these are UI-chrome microcopy (section headers / labels / a11y strings), not
editorial/verdict content:

1. `חזרה ל{categoryNameHe}` — back-link label on the product page (e.g. "חזרה ללחם ומאפים").
2. `התאמת ברקוד מדויקת: מעבר לעמוד המוצר של {name}` — catalog exact-barcode-match jump
   banner (reworded post-gate-fix; see "Gate fixes applied" below — original draft used an
   em-dash and was corrected).
3. `עמוד מוצר ←` — per-row canonical link label (desktop + mobile).
4. `עמוד המוצר` — `title` attribute on the same link.
5. Placeholder/aria text update: `חיפוש שם מוצר, מותג או ברקוד...` (was "חיפוש שם מוצר,
   מותג..."); `aria-label="חיפוש מוצר לפי שם או ברקוד"` (was "חיפוש מוצר").

No new product verdict, claim, or editorial sentence was authored. `rowVerdict`,
`insightLine`, nutrition, ingredients, and methodology text are all rendered verbatim from
existing signed-off VM fields — nothing new was written into those slots.

## OG-image Hebrew rendering: DEGRADED (documented, not silent)

Full Hebrew rendering was not attempted to ship broken glyphs. Verified before building:
`ImageResponse`'s renderer (`@vercel/og`, bundled inside `next/og`) ships its own default
Latin-only font (`node_modules/next/dist/compiled/@vercel/og/Geist-Regular.ttf`) and this
repo has **zero** embeddable Hebrew font files anywhere (checked: no `.ttf`/`.otf`/`.woff*`
under `public/` or elsewhere in the repo — the site's own Hebrew body text relies on the
browser/OS system font stack, which `ImageResponse`'s isolated Satori renderer cannot reach).
Per the task spec's explicit instruction ("if reliable Hebrew rendering proves impractical in
this build pass, DEGRADE to a clean branded template ... rather than shipping broken
glyphs"), the OG image renders **Latin + numeric only**: "Bari" wordmark, the score, "Grade
{A–E}", and the barcode digits. The product's Hebrew name is **not** in the image — it is
correctly rendered as plain Hebrew text in the page's own `<title>`/`<meta>` tags (verified in
`generateMetadata()`), so search/social crawlers still see the correct Hebrew title/description
even though the shared PNG card is script-neutral. Screenshot:
`TASK-471_screenshots/product_og_image.png` (score 95 / Grade A / barcode 7290016245325,
rendered cleanly, no tofu boxes).

If full Hebrew OG rendering becomes a requirement, the fix is straightforward but out of this
pass's scope: source/license a Hebrew-capable font file (e.g. a static Rubik/Heebo/Noto Sans
Hebrew weight), commit it under `public/fonts/`, and pass it via `ImageResponse`'s `fonts`
option — no architecture change needed, `opengraph-image.tsx` already has the `barcode` param
plumbed through.

## Build oracle

Run from `C:\Bari\bari-web`:

- `npx tsc --noEmit` → **exit 0**, zero output (clean).
- `npx next build` → **exit 0** (confirmed via `echo $?` after a dedicated run). Tail:
  ```
  ├ ● /p/[barcode]
  │ ├ /p/7290016245325
  │ ├ /p/3268429
  │ ├ /p/3268252
  │ └ [+184 more paths]
  ├ ƒ /p/-/opengraph-image
  ...
  ●  (SSG)      prerendered as static HTML (uses generateStaticParams)
  ```
  187 total static `/p/[barcode]` pages generated (3 shown + 184 more), 0 TypeScript errors,
  0 build errors. No other route's output changed.

Runtime verification (Playwright against `next start` on a local port, not just the build
log):
- `/p/7290016245325` (mobile 390×844): renders correctly, RTL intact,
  `document.documentElement.scrollWidth === clientWidth === 390` → **zero horizontal
  scroll**, confirmed programmatically, not eyeballed.
- `/p/7290016245325` (desktop 1440×900): renders correctly, header/nav present, layout
  matches the catalog's card language (rounded-18px white cards, hairline borders).
- `/p/0000000000000` (barcode not in the corpus): **HTTP 404**, confirmed via
  `page.goto().status`.
- `/p/7290016245325/opengraph-image`: **HTTP 200**, PNG renders as described above.
- `/catalog`: typing the exact barcode `7290016245325` into the search box surfaces the
  exact-match jump banner and filters the table to 1 row; every unfiltered row (187/187)
  shows the new "עמוד מוצר ←" link pointing at its own `/p/[barcode]`.
- Console/network check: two `400` responses were observed on `/p/[barcode]`, both from
  `/_next/image?url=%2Fbari-logo-optimized.webp...` (the header logo's Next Image optimizer
  under local `next start`). Verified **pre-existing and unrelated to this task** — the
  identical 400 reproduces on `/catalog` (an untouched route) under the same local-server
  conditions. Not a regression introduced here.

## Barcode coverage — no products excluded

`buildBarcodeProductIndex()` skips any row with a null/absent `sku` (never fabricates a
barcode). Cross-checked against the live corpus: the catalog's own unfiltered count reads
"187 מוצרים מוצגים" / "187 מוצרים · 7 קטגוריות פעילות" (screenshot:
`catalog_row_product_links.png`), and the build emitted exactly **187** static `/p/[barcode]`
pages. **187 / 187 — every catalog row has a barcode; zero products were excluded from `/p/`
coverage in this corpus.** (If a future category ships products without a scraped barcode,
they will simply have no `/p/` page — the code path is already there, just unexercised today.)

## Screenshots

All under `C:\Bari\tasks\returns\TASK-471_screenshots\`:
- `product_page_mobile_390.png` — product page at 390px (primary launch viewport).
- `product_page_desktop.png` — product page at 1440px.
- `product_og_image.png` — the generated OG PNG (degraded Latin/numeric template).
- `catalog_barcode_search.png` — catalog search box with an exact barcode typed in, showing
  the jump banner + filtered result.
- `catalog_row_product_links.png` — catalog table (unfiltered) showing the new "עמוד מוצר ←"
  link on every row.

## Scope discipline / things NOT done (explicitly out of lane)

- No new editorial/verdict copy was authored anywhere — every consumer-facing sentence on
  the product page is a verbatim read of an already-signed-off VM field.
- No score/grade/nutrition computation, rounding, or reordering was added — `ScoreChip`,
  `ExpansionSection`, and the loader join are 100% display/lookup.
- No OFF or non-scrape data source was touched, referenced, or introduced anywhere in this
  change.
- Did not touch `ScoreChip`'s or `InventoryGradeChip`'s existing grade-color-coded
  backgrounds — that's pre-existing shipped behavior in components this task was told to
  reuse, not redesign; flagging it here only for visibility, not fixing it (out of scope).
- Did not modify any legacy-quarantined file (`bari-grade-badge.tsx`,
  `dimension-bars.tsx`, `bari-interpretation-panel.tsx`, anything under
  `src/components/snack/`).

## Gate fixes applied (Design critic GO_WITH_FIXES)

The Design vision-critic returned **GO_WITH_FIXES** on the first pass. Three fixes applied
in the same files, all re-verified against the live rendered page (not just source-read):

1. **HIGH — WCAG contrast.** `src/app/p/[barcode]/page.tsx` (~line 137): the category-name
   link color changed from `#1F8F6A` (measured 4.04:1 on white, below the 4.5:1 AA floor) to
   `#167A58` (the vetted brand-line green used two lines below). Re-measured on the live
   rendered page via `getComputedStyle` + a WCAG relative-luminance contrast calculation:
   **`rgb(22, 122, 88)` vs white → 5.30:1** — passes AA. Also swapped the em-dash separators
   in the same file's `generateMetadata()` title/description (`${name} — ברי` →
   `${name} · ברי`, and the description's ` — ` → ` · `) — these are rendered/crawled
   user-facing text (page `<title>`/meta description), so they fall under the same
   minimize-em-dash rule the coordinator flagged for Fix 2, even though the critic's note
   only named the catalog banner explicitly.
2. **Em-dash removal.** `src/components/inventory/product-table.tsx`: the exact-barcode jump
   banner reworded from `נמצאה התאמת ברקוד מדויקת — מעבר לעמוד המוצר של {name}` to
   `התאמת ברקוד מדויקת: מעבר לעמוד המוצר של {name}` (colon variant — kept the "exact match"
   cue per the coordinator's second option). Re-verified on the live page: banner
   `innerText` contains no `—` character.
3. **Test coverage.** Added `/p/7290016245325` to:
   - `e2e/a11y.spec.ts` `ROUTES` — axe-core WCAG2 A/AA gate now covers the product page (this
     is the check that would have caught Fix 1's contrast miss had it existed before).
   - `e2e/visual.spec.ts` `ROUTES` (as `{ path: "/p/7290016245325", name: "product-page" }`)
     — not added to `COMPARISON_ROUTES` (single-product page, not a shelf; the multi-grade-
     chip-count assertion doesn't apply) or `CAROUSEL_PAGES`. Follows the same
     `toHaveScreenshot`/`toMatchSnapshot` path as the existing desktop comparison routes and
     mobile full-page routes. **No baseline snapshot was generated in this pass** — per the
     file's own documented workflow, baselines are created with
     `npx playwright test e2e/visual.spec.ts --update-snapshots --project=mobile` (and
     `--project=desktop`), reviewed, and committed; that is a one-time human-reviewed step
     the orchestrator/Design owner should run once, not something to fabricate here as a
     "passing" baseline against my own uncommitted change.

### Re-verify results

- `npx tsc --noEmit` → **exit 0**, zero output.
- `npx next build` → **exit 0**; still exactly **187** static `/p/[barcode]` pages (3 named +
  184 more in the build tail, unchanged from before the fixes).
- Contrast re-measured live (Playwright + WCAG relative-luminance formula, not eyeballed):
  category-name link = `rgb(22, 122, 88)` → **5.30:1** against white (≥4.5:1 AA pass).
  Confirmed the color attaches to the correct element (`href` starting with
  `/hashvaot/bread?product=...`, text "לחם ומאפים"), not a sibling node.
  script: `verify_fixes.py` (scratch, not committed to the repo).
- Em-dash check: catalog banner `innerText` = `'התאמת ברקוד מדויקת: מעבר לעמוד המוצר של לחם
  טחינה פרוס'` — contains no `—`. Confirmed programmatically (`"—" not in text`).

## Files changed (repo-relative to `bari-web/`)

New:
- `src/app/p/[barcode]/page.tsx`
- `src/app/p/[barcode]/opengraph-image.tsx`
- `src/app/p/[barcode]/_expansion-client.tsx`

Edited (additive only):
- `src/lib/inventory/loader.ts` — added `BarcodeProductEntry`, `buildBarcodeProductIndex()`,
  `getProductByBarcode()`. No existing export changed.
- `src/components/inventory/product-table.tsx` — added barcode to search haystack, exact-match
  jump banner, per-row `ProductPageLink`. No existing prop/behavior removed. (Gate-fix pass:
  banner copy reworded to remove an em-dash.)
- `e2e/a11y.spec.ts` — gate-fix pass: added `/p/7290016245325` to `ROUTES`.
- `e2e/visual.spec.ts` — gate-fix pass: added `/p/7290016245325` to `ROUTES` (baseline
  snapshot not yet generated — see "Gate fixes applied" above).

Edited again in the gate-fix pass (was already listed above as new/edited):
- `src/app/p/[barcode]/page.tsx` — category-link color `#1F8F6A` → `#167A58`; em-dash →
  middle-dot in `generateMetadata()`'s title/description.

---

```json
{
  "task": "TASK-471",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/src/app/p/[barcode]/page.tsx",
      "sha256": "b381820d6ac346d0d88599d2ca4eecefe091dff057c093c542f73970b21df1e7",
      "action": "modified"
    },
    {
      "path": "bari-web/src/app/p/[barcode]/opengraph-image.tsx",
      "sha256": "c1ef073babdbface98172651b7d3c3109df864c5b218f837d63284113ea5d102",
      "action": "created"
    },
    {
      "path": "bari-web/src/app/p/[barcode]/_expansion-client.tsx",
      "sha256": "d3aefbe3061db4ad7ff60b75275334c72f61137c253fe3da84973206f7b1bb75",
      "action": "created"
    },
    {
      "path": "bari-web/src/lib/inventory/loader.ts",
      "sha256": "6ee68c26e3350e6601349cadaaeb2652fab503d9dc51645f5110ab7f0e5e4ed0",
      "action": "modified"
    },
    {
      "path": "bari-web/src/components/inventory/product-table.tsx",
      "sha256": "d9b9c413813914998c71712cb804686d014e6459aa015dfae0712ca529c4c3b3",
      "action": "modified"
    },
    {
      "path": "bari-web/e2e/a11y.spec.ts",
      "sha256": "76b43ccdd398949b342213593ce4377be28246c050ff6d58db027edd11fe1f67",
      "action": "modified"
    },
    {
      "path": "bari-web/e2e/visual.spec.ts",
      "sha256": "40e74b6662aa66e54bd5a2730b65eec33d6e0fa7bec2f57a7d9426d41e448e31",
      "action": "modified"
    },
    {
      "path": "tasks/returns/TASK-471_screenshots/product_page_mobile_390.png",
      "sha256": "47bcb14367a6721cb7ef25b0da554bd6d3ddd4cae2b4e18012dde1b66da2267a",
      "action": "created"
    },
    {
      "path": "tasks/returns/TASK-471_screenshots/product_page_desktop.png",
      "sha256": "f8a84cc5e6df5f7872138d02204d8a584f4861455958da77ba16c8ffab98c710",
      "action": "created"
    },
    {
      "path": "tasks/returns/TASK-471_screenshots/product_og_image.png",
      "sha256": "881e0ad684917c25bbed9feedc48ce97656c614a3b79de25e8b520e8199cca9d",
      "action": "created"
    },
    {
      "path": "tasks/returns/TASK-471_screenshots/catalog_barcode_search.png",
      "sha256": "d6b349d45fa2e557649ba267874e3735809e9234f9c042e748431a2396bb0eb3",
      "action": "created"
    },
    {
      "path": "tasks/returns/TASK-471_screenshots/catalog_row_product_links.png",
      "sha256": "8b0e09d81aef64231ceae69f8e93cb2da5ce7b203c6f705f439847cbb7ce2683",
      "action": "created"
    }
  ],
  "counts": {
    "static_product_pages_generated": { "value": 187, "denominator": "catalog_total_products_187", "source": "next_build_output_line_count + catalog_header_display", "distribution": "full_set_not_sampled" },
    "products_excluded_for_null_barcode": { "value": 0, "denominator": 187, "source": "static_page_count_equals_catalog_total" },
    "new_hebrew_ui_strings_introduced": { "value": 5, "denominator": "5_listed_in_return_body", "source": "manual_diff_of_authored_strings" },
    "tsc_errors": { "value": 0, "denominator": "full_project_typecheck" },
    "build_errors": { "value": 0, "denominator": "full_next_build" },
    "console_400s_on_new_route": { "value": 2, "denominator": "next_image_optimizer_preexisting_confirmed_on_untouched_route", "source": "playwright_response_listener" },
    "gate_fixes_applied": { "value": 3, "denominator": "3_requested_by_design_critic", "source": "diff_against_critic_list" },
    "category_link_contrast_ratio": { "value": 5.30, "denominator": "4.5_wcag_aa_floor", "source": "playwright_getComputedStyle_plus_wcag_relative_luminance_formula" },
    "em_dashes_remaining_in_touched_rendered_strings": { "value": 0, "denominator": "all_rendered_or_metadata_strings_authored_in_this_task", "source": "grep_plus_live_innerText_check" }
  },
  "commands_run": [
    { "cmd": "npx tsc --noEmit", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 },
    { "cmd": "npx next build", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 },
    { "cmd": "npx next start -p 3471 (first pass, screenshots)", "cwd": "C:\\Bari\\bari-web", "exit_code": "backgrounded, stopped manually" },
    { "cmd": "python shoot_p471.py / shoot_p471b.py / shoot_p471c.py / shoot_p471d.py (playwright: screenshots, 404 check, 400-source isolation)", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 },
    { "cmd": "npx tsc --noEmit (post-gate-fix re-verify)", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 },
    { "cmd": "npx next build (post-gate-fix re-verify)", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 },
    { "cmd": "npx next start -p 3473 (post-gate-fix re-verify server)", "cwd": "C:\\Bari\\bari-web", "exit_code": "backgrounded, stopped manually" },
    { "cmd": "python verify_fixes.py (playwright: live contrast measurement + em-dash check)", "cwd": "C:\\Bari\\bari-web", "exit_code": 0 }
  ],
  "not_done": [
    "Full Hebrew glyph rendering inside the OG PNG — degraded to Latin/numeric per the spec's explicit fallback clause; documented fix path given (embed a Hebrew font file under public/fonts/).",
    "ScoreChip / InventoryGradeChip grade-color-coded backgrounds were not changed — pre-existing behavior of components this task reused, not built; flagged for visibility only, no action taken (out of scope).",
    "e2e/visual.spec.ts baseline snapshot for the new product-page route was NOT generated in this pass — per the file's own documented workflow this is a one-time --update-snapshots step that should be run and reviewed once by the owner/orchestrator, not fabricated here against my own uncommitted change."
  ],
  "self_check": {
    "tsc_exit_0": true,
    "build_exit_0": true,
    "static_product_pages_count_unchanged_after_fixes": true,
    "fix1_contrast_measured_live_ge_4_5": true,
    "fix1_contrast_value": "5.30:1",
    "fix2_em_dash_absent_in_banner_innerText": true,
    "fix3_route_added_to_a11y_spec": true,
    "fix3_route_added_to_visual_spec": true,
    "fix3_visual_baseline_generated": false,
    "no_legacy_quarantined_file_touched": true,
    "no_off_source_referenced": true
  },
  "return_contract_version": "v1"
}
```
