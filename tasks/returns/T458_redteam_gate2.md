# TASK-458 — Adversarial QA / Red-Team gate (gate 2 of 2): /catalog first go-live

**Task:** TASK-458 (Adversarial QA sign-off, gate 2 of 2)
**Branch:** `golive/catalog-task458` (worktree `C:\bari_wt_t458`, baseline `origin/master` `48811ebb`)
**Challenger:** adversarial-qa-agent (independent — read artifacts + rendered DOM directly; did not accept builder summaries)
**Date:** 2026-07-02
**Scope:** `/catalog` (new public route), header nav, blog/comparison OG fixes, barcode search, catalog copy

---

## VERDICT

**GO_WITH_FIXES**

The package is **render-verified, build-clean, data-consistent, and OFF-clean.** The shipped `/catalog`
page is internally honest and correctly matches the live comparison pages. **Zero CRITICAL findings** —
nothing blocks go-live on a correctness or defensibility basis.

The fixes below are **return-hygiene and pre-merge cleanups**, not page defects. The single item the owner
should consciously accept before merge is the public cadence commitment **"הקטלוג גדל כל שבוע"** (F-C1).

Required before merge (GO_WITH_FIXES list):
1. **F-V1 (HIGH):** Correct the return's headline product count — the shipped catalog renders **187**, not 209.
2. **F-C1 (MEDIUM, owner-accept):** Confirm the owner will keep the public weekly-growth promise, or soften the copy.
3. **F-V2 / F-V3 / F-C2 (MEDIUM):** stale loader doc-comment, one branch-introduced a11y lint warning, on-page "what is Bari" explainer. Document or monitor.

---

## TRACK V — VERIFICATION (deterministic)

| Gate | Result | Observed value |
|---|---|---|
| `npm run build` | **PASS** | exit 0; `/catalog` emitted as `ƒ /catalog` (dynamic) |
| `/catalog` renders (real DOM, `next start` :3699) | **PASS** | HTTP **200**, 805,101-byte HTML, product table painted (40 grade-chip aria labels in DOM), `dir="rtl"` present (8 containers), H1 `קטלוג המוצרים` present |
| Grade chips present | **PASS** | `דרגה A/B/…` aria-labels rendered; 0 `לא נוקד` (no unscored in corpus) |
| Blog `og:image` fix | **PASS** | `/blog/food-dyes` renders `og:image = https://bari.digital/bari-logo-optimized.webp` (was absent — the bug fixed) |
| Comparison `og:title` page-specific | **PASS** | `/hashvaot/hummus` → `השוואת חומוס \| Bari`; `/hashvaot/juices` → `השוואת מיצים ומשקאות פירות \| Bari` (not the site default) |
| OG metadata regression (byte-diff titles/descriptions) | **PASS (with note F-V3-adjacent)** | bread/milk/food-dyes strings byte-identical, only wrapped in helper. **Juices rendered description changed 65→17** — this is a **correction** of a pre-existing stale inline literal in `page.tsx` (the data-source const already said 17); net beneficial, not a regression |
| Data integrity — product count vs corpus | **FAIL→explained (F-V1)** | Rendered `summary.totalProducts = 187`, categoryCount = 7. Return claimed 209. Gap = 22 = hummus raw 57 vs curated 35 (TASK-100 vegetable-spread/partial-data exclusion, applied by `getHummusCorpusPayload`). **187 is correct**; 209 = raw `products[]` sum without curation. |
| Grade-transformation drift (S grade) | **PASS (not a defect)** | Corpus JSON carries `grade:"S"` for score≥90 (e.g. `bsip1_bread_7290016245325`, 94.8). Catalog shows **A**. Verified `/hashvaot/bread` JSON-LD reports the **same product as grade "A"** → the S≥90→A fold is the site-wide `normalizeGrade` in `corpus.ts` (5-grade consumer scale), applied to every comparison page. **Catalog is consistent with the live comparison surface. No cross-surface inconsistency.** |
| Spot-check fidelity (5+ products, name/brand/grade/score/retailer/sku) | **PASS** | First bread row rendered `name=לחם טחינה פרוס, score=94.8, grade=A, sku=7290016245325, retailer=שופרסל` — matches `bread_frontend_v4.json` (raw grade S normalized to A per above). No product shows another category's data (`categoryId`/`categoryNameHe`/`comparisonHref` all self-consistent per row). |
| Retailer resolution | **PASS** | All 187 rows resolve to `shufersal` (snacks via documented BSIP0 category override; others carry retailer). `retailerBreakdown` = 1 entry (shufersal, 187), 0% "other" — under the 5% warning threshold. |
| Search — barcode exact | **PASS (code-verified)** | `product-table.tsx:481-498` — digit query, whitespace-stripped, exact-matched against whitespace-stripped `sku` → returns row. |
| Search — whitespace-padded barcode | **PASS** | `rawQ.replace(/\s+/g,"")` on both query and sku (`:482`, `:497`). |
| Search — Hebrew name substring | **PASS** | `haystack = [name, brand, categoryNameHe, retailerNameHe, sku].join(" ").toLowerCase()`, `includes(q)` (`:500-503`). |
| `npm run lint` | **exit 1 — CONFIRMED PRE-EXISTING** | All 8 error-level (exit-1-causing) files are pre-existing & untouched by this branch (privacy, terms, e2e/vision-probe, olive-oil-transparency-matrix, consent-manager, ga4-script, public/hero/*). Branch added exactly **1 new lint item, a WARNING** (F-V3), not an error. |
| OFF-ban grep (catalog/inventory code) | **PASS** | Zero OFF residue in `src/lib/inventory/*`. Only hit is the substring "off the" in a doc comment (false positive). Retailer/data path sources exclusively from registry corpus VMs. |
| Header nav link | **PASS** | `href="/catalog"` present in rendered site-header; label `קטלוג` matches sibling nav labels. |

**Track V status: GREEN** (the two FAIL-looking rows both resolve to correct-page / accurate-data; the sole
true defect is a wrong number in the *return*, not on the page → F-V1).

---

## TRACK C — CHALLENGE (adversarial defensibility)

### Consumer-string leakage gate
Ran `hebrew_readability.analyze(...).is_clean` on every new/changed consumer string
(meta description, empty-state heading + body, dormant buy tooltip, subtitle): **all `is_clean=True`.**
No framework vocabulary, no raw-score mechanics, no recommendation language.

### Q7 — "המוצרים שבארי כבר בדקה… הקטלוג גדל כל שבוע" (grows every week)
- **"המוצרים שבארי כבר בדקה"** (products Bari has *already* checked): **defensible.** Honestly scopes the set
  as a subset, not "all." Directly fixes the pre-fix "כל המוצרים" overreach. Matches the on-page subtitle
  which states the real counts (187 / 7).
- **"הקטלוג גדל כל שבוע"** (the catalog grows every week): **plausible-but-a-public-commitment (F-C1).** Recent
  git history shows a roughly-weekly go-live cadence (crackers, cheese de-anchor, de-anchor sweep, chocolate
  in the recent window), so the claim is *currently true*. But it converts internal momentum into a **standing
  public cadence promise** that becomes false the first quiet week. No health/score claim, easily softened.
  → **Owner should consciously accept or soften.**

### Q8 — dormant "צפייה ברשת · בקרוב" buy affordance
**Defensible.** Rendered DOM: 20 buttons on page 1, all `disabled`/`aria-disabled="true"`, tooltip
`בקרוב — צפייה במוצר באתר הרשת`, greyed at `--fg3` (WCAG-passing per the Design audit noted in-file). **Zero
active external buy links, zero external retailer hrefs.** It reads as an explicit "coming soon," not a broken
control (disabled state + text + tooltip all agree). This is an honest signal of a real roadmap slot, not a
dark pattern.

### Q9 — first-visit comprehension + path to deep content
- **Path to deep content: PASS (strong).** 227 per-product deep links `(/hashvaot/{cat}?product={id})`,
  42 `/hashvaot` links, sidebar `השוואות` nav, 2 blog links, 1 methodology link. Every row is a doorway into
  its full comparison page. No dead end.
- **"What is Bari" in seconds: PARTIAL (F-C2, MEDIUM).** The page body leads with "BARI CATALOG" / H1
  "קטלוג המוצרים" / counts + a grade donut, but **no one-line on-page explainer** of what a Bari grade means
  or that Bari scores nutrition independently. A visitor arriving cold from the sitemap sees a graded table
  with no in-context definition of the grade. Mitigated by the site-header context and the meta description
  (search snippet), and the deep links are one tap away — hence MEDIUM, not blocking.

### Q10 — 7-of-registry coverage gap: ship or wait?
**Ship (defensible).** The catalog surfaces the **7 registry-registered scored categories = 187 products**;
~14 other `/hashvaot` routes (incl. static stubs like personal-care/supermarket/supplements) are not in it.
With the honesty fixes already applied — subtitle states real counts, empty-state says "המוצר עדיין לא נבדק"
and links to `/hashvaot`, description scopes to "already checked" — shipping a partial-but-honest catalog is
**more defensible than waiting** for full coverage. It never claims completeness; the growing-subset framing is
truthful. The only residual exposure is the cadence promise (F-C1).

**Track C status: zero CRITICAL, zero HIGH-blocking; findings are MEDIUM/monitor.**

---

## FINDINGS BY SEVERITY

### CRITICAL — none.

### HIGH
- **F-V1 — Return headline count is wrong (209 vs shipped 187).** The P458 return and its `counts` block claim
  `catalog_products: 209/209` and a grade distribution including `S:2 … C:73 D:54`. The **rendered catalog
  serializes `totalProducts:187`** with distribution `{A:15,B:49,C:64,D:41,E:18,unscored:0}` (no S — S folds
  to A on the consumer scale). Root cause: the return summed raw `products[]` array lengths (hummus 57) instead
  of the curated payload the loader actually ships (hummus 35, per TASK-100 exclusions) and read raw JSON grades
  instead of the normalized consumer grades. **The page is correct; the return's numbers are not.**
  *Implication:* an inaccurate count/distribution in the closing record; a reviewer trusting the return would
  cite a wrong corpus size publicly. *Evidence:* rendered RSC payload `\"totalProducts\":187`, topCategories
  hummus `count:35`; `corpus.ts:42-73 normalizeGrade`; `hummus-comparison-page-data.ts:95-96` exclusions.
  *Routes to:* **data-agent / frontend-agent** (correct the return + counts before the orchestrator closes;
  no code change required — the shipped number is right).

### MEDIUM
- **F-C1 — "הקטלוג גדל כל שבוע" is a public cadence commitment.** True today, but a standing promise that turns
  false on a quiet week. No health/score claim; trivially softened. *Routes to:* **content-agent / product-agent
  (owner-accept).**
- **F-V2 — Stale loader doc-comment.** `src/lib/inventory/loader.ts:235,240` says "174 catalog rows" and "6
  registered categories"; actual is 187 rows / 7 categories. Comment-only; zero runtime effect (loader is
  registry-driven). *Routes to:* **frontend-agent.**
- **F-V3 — One branch-introduced a11y lint WARNING.** `src/components/inventory/top-categories-card.tsx:110` —
  `aria-pressed` is not supported by role `listitem` (`jsx-a11y/role-supports-aria-props`). Does not cause the
  exit-1 (that is all pre-existing), but it is a real a11y defect this branch added. *Routes to:* **frontend-agent.**
- **F-C2 — No on-page "what is Bari" explainer on /catalog.** First-visit comprehension is only partially met
  on-page; deep content is reachable (227 deep links) so not a dead end. *Routes to:* **content-agent / design-agent.**

---

## MECHANICAL GATE NOTES
- Build oracle re-verified independently: `npm run build` exit 0; `/catalog` 200 in real DOM.
- Lint claim independently attributed: 0 error-level lint in branch-touched files; 1 new warning (F-V3).
- OG regression independently byte-diffed against `origin/master`: no title/description string regressed
  (juices 65→17 is a correction).
- Leakage gate (`hebrew_readability`) run on all new strings: all `is_clean`.

---

```json
{
  "task": "TASK-458",
  "gate": 2,
  "role": "adversarial-qa-agent",
  "verdict": "GO_WITH_FIXES",
  "proposed_status": "RETURNED",
  "critical_open": 0,
  "findings": {
    "HIGH": ["F-V1 return headline count 209 vs shipped 187 (page correct, return wrong)"],
    "MEDIUM": [
      "F-C1 'grows every week' public cadence commitment (owner-accept)",
      "F-V2 stale loader doc-comment 174/6 vs 187/7",
      "F-V3 branch-introduced a11y lint warning top-categories-card.tsx:110",
      "F-C2 no on-page 'what is Bari' explainer on /catalog"
    ]
  },
  "track_v": "GREEN",
  "track_c": "zero CRITICAL, zero blocking HIGH",
  "counts": {
    "catalog_products_rendered": "187 (summary.totalProducts in served RSC payload; per-cat bread:23 snacks:21 hummus:35 cheese:47 breakfast-cereals:20 granola:22 crackers:19)",
    "catalog_categories_rendered": "7 (summary.categoryCount)",
    "grade_distribution_rendered": "A:15 B:49 C:64 D:41 E:18 unscored:0 (no S — folds to A on 5-grade consumer scale)",
    "products_spot_checked": "6/6 corpus-vs-render match (grade normalized per corpus.ts)",
    "og_pages_verified": "3/3 (food-dyes og:image present; hummus+juices og:title page-specific)",
    "lint_error_files_branch_introduced": "0/8 (all pre-existing)",
    "lint_warnings_branch_introduced": "1 (F-V3)",
    "new_consumer_strings_leakage_clean": "5/5 is_clean=true",
    "dormant_buy_buttons_rendered": "20/20 disabled, 0 active external links",
    "deep_comparison_links_on_catalog": "227"
  },
  "commands_run": [
    { "cmd": "npm run build (bari-web/, worktree)", "exit_code": 0 },
    { "cmd": "npx next start -p 3699 + Invoke-WebRequest /catalog", "exit_code": 0, "http": 200 },
    { "cmd": "Invoke-WebRequest /hashvaot/bread /hashvaot/hummus /hashvaot/juices /blog/food-dyes", "exit_code": 0, "http": 200 },
    { "cmd": "npm run lint (bari-web/, worktree)", "exit_code": 1, "note": "all error-level files pre-existing; 0 branch-introduced errors" },
    { "cmd": "node corpus product-count per category", "exit_code": 0 },
    { "cmd": "hebrew_readability.analyze on 5 new strings", "exit_code": 0 }
  ],
  "not_done": [
    "fixes (out of lane — findings routed, not fixed)",
    "push/PR/deploy (out of lane)",
    "task close (orchestrator only)"
  ],
  "self_check": "Rendered /catalog served 200 with product table painted; summary.totalProducts=187 read directly from the served RSC payload; grade 'A' for bsip1_bread_7290016245325 cross-verified in /hashvaot/bread JSON-LD; lint error attribution computed from lint.log vs git diff --name-only origin/master...HEAD."
}
```
