# TASK-602 Milk Pilot — full-traceability re-scrape (data-agent, 2026-07-11)

Scope: prove the re-scrape -> retain -> manifest -> verify loop end-to-end on the
milk shelf (18 served products, 0/18 stored raw captures per TASK-601) before
fanning out to the other 380 no-capture products.

## Process note (branch state)

`03_operations/bsip0/manifest/{build_manifest.py, build_census.py, replay_harness.py,
capture_manifest.json, replay_baseline.jsonl}` did not exist on `task506` (this branch
forked before TASK-601's manifest work landed on `origin/master` at `f6c5206d`; only
the census-summary commit `ee6f64d8` was present, without the actual tooling). These
5 files were ported verbatim from `origin/master` (pure additions, zero conflicts —
confirmed via `git diff HEAD origin/master --stat` before porting) so the tools this
task depends on actually exist locally. Flagging per spec-conflict duty: the task
assumed these scripts were runnable in-place; they were not, on this branch, until
ported.

Re-running `build_manifest.py` rescans the ENTIRE current tree (not incremental), so
its headline numbers (893->2456 total captures) reflect this branch's larger corpus
state, not milk alone — the milk-specific delta is isolated below.

## Spec correction: not all 18 barcodes are Israeli 7290 GTINs

The task brief assumed all 18 served milk barcodes are Israeli (729x…) GTINs. 5/18
are not:
- `5411188124689`, `5411188112709`, `5411188300328` — GS1 prefix 541 (Belgium; Alpro-style
  plant-drink barcodes).
- `8000215204554`, `8000215204219` — GS1 prefix 800 (Italy; Isola Bio-style rice-drink
  barcodes).

This is NOT an OFF-ban violation — these are legitimately imported products keeping
their manufacturer's home-country barcode (normal retail practice for imports), and
all 5 scraped cleanly from the live Israeli Shufersal storefront under that exact
barcode. Distinct from the (unrelated, untouched) synthetic placeholder barcodes in
`02_products/milk_and_alternatives/observations_bsip0/` (`5411188001001` etc. —
sequential fakes, not the real served barcodes, not read for this task).

## Scrape results (18 targets, Shufersal-first, retailer fleet fallback, ~1 req/sec)

| Retailer | Found | Notes |
|---|---:|---|
| Shufersal (direct barcode URL) | 15/18 | all with a usable nutrition panel |
| Hazi Hinam (fallback, dairy category API) | 1/18 | `7290000051352` — identity + ingredients ("חלב") confirmed, but GS1 panel has ZERO nutrition rows on this retailer |
| Tiv Taam (fallback, product-search API) | 1/18 | `7394376619939` — full 14-row nutrition panel |
| Not found anywhere checked | 1/18 | `7290119385560` (Alpro soy barista 500ml) — 404 on Shufersal, no match in Hazi Hinam's dairy subcategory, no barcode match among 40 Tiv Taam "בריסטה" search results (candidates included 3 *other* Alpro soy-barista barcodes, not this one). Genuine NOT_FOUND — not invented, not OFF-filled. |

Additionally, one Shufersal-scraped product (`7290014760141`, almond drink) resolved
to **zero usable nutrition rows** despite `status=scraped`: the page carries 2 competing
nutrition tables (`"כוס"` per-serving + `"100 מ״ל"` per-100ml) and the shared parser's
`_PER_100G_MARKERS` (`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`) does not
recognize a `"100 מ"ל"` (per-100ml, liquid) header as the per-100g-equivalent basis —
only gram-based headers. With no table classified `per_100g`, the multi-table selector
correctly refuses to guess (`insufficient=True`) and returns empty rows. **Finding, not
fixed here** (shared module, affects every retailer scraper, out of this pilot's "no
changes" scope) — recommend a follow-up task to extend the per-100g basis recognizer to
accept per-100ml liquid headers; likely affects juices and other liquid categories too.

**Net: 17/18 barcodes resolved on some retailer (identity); 16/18 usable nutrition
panels (excludes the Hazi Hinam empty-panel and the genuine not-found); 15/18 scored
against publish for material fidelity below (excludes the 2 with no usable panel plus
the 1 not-found = 3 excluded, 15 evidence-backed comparisons).**

Retention: `02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/`
(`milk_rescrape_final.json` = consolidated per-barcode records with
`nutrition_raw_source.rows`, retailer, source_url, scrape_timestamp, ingredients_raw —
scannable by the manifest builder; `milk_rescrape_diff.json` = the verify step below;
`milk_rescrape_captures.json` / `hazi_hinam_7290000051352.json` /
`tivtaam_lookup_results.json` = intermediate per-retailer raw process files, kept for
audit trail).

## Manifest + coverage (before -> after)

| | Before (TASK-601) | After (this pilot) |
|---|---:|---:|
| milk_frontend_v1 HAS_CANONICAL_CAPTURE | 0/18 | **17/18** |
| milk_frontend_v1 NO_CAPTURE | 18/18 | **1/18** (`7290119385560`, genuine not-found) |

Verified independently by re-deriving the canonical-GTIN set from the freshly rebuilt
`03_operations/bsip0/manifest/capture_manifest.json` and checking each of milk's 18
`barcode` values against it directly (not just trusting `build_census.py`'s printed
number) — same 17/18 result both ways.

Note: canonical-capture membership only requires a `nutrition_raw_source.rows` LIST
(builder's own membership policy) — it does not require the list to be non-empty. The
`7290000051352` Hazi Hinam record counts toward the 17/18 by this rule despite carrying
zero nutrition rows (identity/ingredients only). Treat "17/18 HAS_CAPTURE" as a
manifest-membership number; "16/18 usable nutrition panel" is the tighter,
verification-relevant number.

Full corpus-wide (all shelves, this branch's current tree): total captures 893->2456,
canonical 807->1263, distinct GTINs 652->1070, served-product coverage 359/757->505/710
(denominator also shifted because served product counts differ slightly on this
branch). `03_operations/reports/task601_bsip0_census.md` was regenerated in place (that
is its designated, shared output path) — the large jump reflects this branch's fuller
corpus state versus origin/master at TASK-601 close, not a single-step miracle; the
milk-specific 0/18->17/18 delta above is the number this task is actually answerable
for.

## Verify: captured vs published (15 evidence-backed products, thresholds per TASK-595:
MATCH <=0.05g/0.5mg-kcal, ROUNDING <=0.15g/2mg-kcal, MATERIAL above; FIELD_GAP = one
side null; NO_EVIDENCE = no usable panel)

Disposition: FULLY_MATCH 14/15, MATERIAL_PRODUCT 1/15, (+2/18 NO_COMPARABLE_FIELDS —
the 2 products with zero usable rows — and 1/18 NO_EVIDENCE — the not-found product).

**Per-field fidelity on the fields that ARE published (comparable-both-sides only):**
- energyKcal: 15/15 MATCH
- sodium: 13/13 MATCH
- sugar: 7/7 MATCH
- protein: 14/15 MATCH, **1/15 MATERIAL**

**TRIPWIRE-1 — MATERIAL discrepancy, live-verified, STOPPING here per instruction:**

Product `8000215204554` (משקה אורז קוקוס אורגני / organic rice-coconut drink, Vitariz,
currently `score=48.1, grade=D, rank=14/18`): published `expansion.nutrition.protein =
0.4`. Fresh Shufersal scrape of the SAME barcode, same URL
(`.../p/P_8000215204554`), raw row `{"value":"0","unit":"גרם","label":"חלבונים"}` (the
Hebrew "proteins" row, read directly, no ambiguity) -> replayed `protein_g = 0.0`.
Delta = 0.4g > the 0.15g MATERIAL threshold.

This is not a cosmetic field — the shipped consumer copy cites "0.4 ג׳ חלבון" **three
times** as the load-bearing reason for the D grade (`insightLine`, `rowVerdict`, and
`limitingFactors[0]` all quote the exact figure "0.4 ג׳ חלבון בלבד"). If 0.0 is the
correct live value, every citation of the number is currently wrong, and protein is a
scored BSIP2 dimension for this category (it's on the product's own `metrics` block).
Movement table:

| Field | Published | Live-replayed | Delta | Class | Cited in shipped copy? |
|---|---:|---:|---:|---|---|
| protein (g/100ml) | 0.4 | 0.0 | 0.4 | MATERIAL | Yes — 3x verbatim |

I am NOT computing or asserting a score-delta here — that requires the BSIP2 milk
scoring engine/weights, which is Nutrition Agent territory, not mine to simulate. No
published JSON, score, or grade has been changed. Surfacing per Hard Rule 5/7 and the
task's explicit TRIPWIRE-1 instruction; owning agents should confirm which value (0.4
vs 0.0) is correct before any correction and re-verify whether the D/48.1 and the
copy's 3 citations still hold either way.

## Field-coverage finding (systematic, shelf-wide — not a value error)

Across the 15 evidence-backed products, three fields are published `null` on
**every single product** despite being live-scrapable on every single product checked:

| Field | Published=null but live capture HAS a value | 
|---|---:|
| fat | 15/15 |
| carbs | 15/15 |
| saturated fat | 9/15 (rest genuinely absent on-page too) |
| fiber | 8/15 |
| sugar | 4/15 |
| sodium | 2/15 |

Fat and carbs are 100% missing from the published milk shelf despite being present on
100% of the live pages checked. This is a shelf-wide display/enrichment gap (BSIP1
never captured or never carried these fields through for milk), not a source-data
problem — the data exists and is capturable right now. Flagging per field-coverage
duty; recommend a follow-up BSIP1 re-enrichment task for milk to backfill
fat/saturated-fat/carbs (Nutrition/Product to scope — no scoring change implied by
merely displaying an already-uncaptured field, but that determination is theirs).

## No published-JSON changes

Confirmed: no file under `bari-web/src/data/comparisons/` was modified. `git status`
shows only new files under `02_products/milk_and_alternatives/bsip0_outputs/` and
`03_operations/bsip0/manifest/`, plus the in-place regeneration of
`03_operations/reports/task601_bsip0_census.md` (its designated, pre-existing output
path).
