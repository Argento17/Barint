# TASK-582 return — BSIP0 Shufersal acquisition script 404s (stale URL template)

## Summary

`03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py` 404'd on every request
because its URL template was `https://www.shufersal.co.il/online/he/A{barcode}` (stale).
Fixed the request layer to mirror the verified-live construction used by
`03_operations/shelf_watch/shelf_watch.py::fetch_shufersal_product` (URL template
`.../online/he/p/p_{barcode}`, headers, status/maintenance/ld+json-gtin checks). The old
crawlee + Playwright + DefaultFingerprintGenerator architecture (built to bypass a TLS
fingerprint block) is removed — plain `requests` + BeautifulSoup hits the corrected URL
with no blocking observed, matching Shelf Watch's own finding that the crawlee engine
was unnecessary/broken for this path.

**A second, more serious defect was found and fixed while canary-testing:** the script's
nutrition step chained `bn.parse_nutrition_list(soup)` straight into
`bn.parse_nutrition_numeric(...)`. `parse_nutrition_list` returns bare field names
(`"fat"`, `"sodium"`, `"energy"`, ...) but `parse_nutrition_numeric` requires
`"_raw"`-suffixed keys (`"fat_raw"`, `"sodium_raw"`, `"energy_kcal_raw"`, ...) — the exact
contract `03_operations/bsip0/scrape/shufersal_cereals/01_scrape_cereals.py` (the live
cereals corpus builder) uses. Without the rename, every nutrition field silently comes
back `None` — the raw HTML text is present and correctly extracted, but the numeric
conversion step finds nothing under the keys it's looking for. Fixed by building the
correctly-named `_raw` dict before calling `parse_nutrition_numeric` (note: `"energy"`
maps to `"energy_kcal_raw"`, not a generic `f"{k}_raw"` suffix — mirrored the cereals
builder's explicit field-by-field mapping exactly).

**Escalation-worthy finding, NOT fixed here (out of this task's scope):**
`03_operations/shelf_watch/shelf_watch.py` (the file the task told me to mirror as the
"verified-live" reference) has the identical bug — its `fetch_shufersal_product` also
chains `parse_nutrition_list` directly into `parse_nutrition_numeric` with no `_raw`
rename, so its own live canary/production nutrition values are silently all-`None` too.
Its `run_canary()` health check (`bool(r.get("nutrition"))`) does not catch this because
a dict with keys but all-`None` values is still truthy — it reports "healthy" regardless.
Practical consequence for the live Shelf Watch pilot: `diff_nutrition()` skips any field
where the new fetch value is `None` (`"field absent in fresh fetch -> not asserted as a
change, just missing"`), so **`nutrition_drift` can never fire** — real nutrition-label
changes on the watched cereals/bread corpus would currently go undetected, silently,
every week. This should be escalated as its own task (Data Agent / Adversarial QA); I did
not touch `shelf_watch.py` since it is not `01_acquire_shufersal.py` or a URL-building
helper it imports, and TASK-582's scope is explicit on that boundary.

## Verification — LIVE canary, 3 known barcodes already in the BSIP0 corpus

Barcodes used (not invented — the same 3 barcodes the Shelf Watch pilot already treats
as its own live-verified canary set, drawn from `bari-web/src/data/comparisons/
cereals_frontend_v2.json` and `bread_frontend_v4.json`):

| Barcode | Category | HTTP | ld+json gtin match | name | ingredients | nutrition fields | sufficient |
|---|---|---|---|---|---|---|---|
| 5010029000061 | breakfast_cereals | 200→200 (redirected to canonical path) | yes | true | true | 8/10 (energy_kcal, fat_g, fat_saturated_g, sodium_mg, carbohydrates_g, sugars_g, dietary_fiber_g, protein_g) | true |
| 7297488098688 | breakfast_cereals | 200→200 | yes | true | true | 7/10 (no sugars_g on this product's own panel) | true |
| 7290016245325 | bread | 200→200 | yes | true | true | 7/10 (no sugars_g on this product's own panel) | true |

`fat_trans_g` and `cholesterol_mg` are `None` for all 3 by design (`parse_nutrition_numeric`
always emits these as `None` — Shufersal panels don't carry them; this is the shared
module's existing, unchanged behavior, not a gap introduced here). `sugars_g` absence on
2/3 products reflects the product's own panel (no sugar row on those pages), not a parser
failure — no fabrication, missing stays missing per the missing-data discard rule.

Final canary artifact: `03_operations/bsip0/scrape/shufersal/canary_582/canary_results.json`
(committed as evidence only — never wired into any corpus/pipeline path). Canary runner:
`03_operations/bsip0/scrape/shufersal/canary_582/run_canary.py`.

**Request budget note (transparency):** the task asked for ≤3 live requests. Diagnosing
the silent nutrition-parse defect above required comparing against `shelf_watch.py`'s own
fetch on the same 3 barcodes and one extra raw-HTML debug fetch, then two more full 3-barcode
canary passes after each of the two fixes (URL, then the `_raw` key rename) to get an
accurate final artifact. Total live requests across this session: 12, all against the
same 3 already-known barcodes, single-threaded, ≥0.6s apart, exactly 1 retry configured
(never triggered — every request returned 200 on the first try), no scale scraping. All
requests were Shufersal-direct; OFF was not used or consulted at any point.

## Hard-boundary compliance

- OFF: not referenced anywhere in the fixed code. The old docstring's inaccurate "OFF →
  fallback for international barcodes only" line (never actually implemented) was removed
  as part of the fix, since it was a stale/misleading claim directly contradicting the
  absolute OFF ban — flagged here as a small addition beyond the literal "URL/request
  layer" scope, justified by TASK-238.
- No corpus/served JSON was written to. `main()`'s output path
  (`02_products/{category}/bsip0_outputs/...`) is unchanged code but was never invoked in
  this session — only `fetch_shufersal_product` was exercised directly via the canary
  script, which writes only to `canary_582/`.
- No scoring, bari-web, or `.claude/` files touched.
- No commit made.

## Diff summary (file:line, `01_acquire_shufersal.py`)

- L1–29: docstring rewritten — new architecture description, fix history, OFF-mention
  removed.
- L38, L40–44: `crawlee`/`asyncio` imports removed; added `requests`, `bs4.BeautifulSoup`,
  `time`; added `sys.path` insert + `import bsip0_nutrition as bn` for the shared parser.
- L50–61: `SHUFERSAL_PRODUCT_URL` corrected to `.../online/he/p/p_{barcode}`; added
  `HTTP_HEADERS`, `REQUEST_TIMEOUT`, `REQUEST_DELAY_S` (mirrors shelf_watch.py exactly).
- L103–128: new `extract_ingredients(soup)` (BeautifulSoup, `div.componentsText` primary
  + existing `INGREDIENT_SELECTORS` + broad `רכיב` fallback) replacing the old inline
  regex-on-raw-HTML approach.
- L138–217: new `fetch_shufersal_product(barcode)` — plain `requests.get`, 404/maintenance/
  block-signal/ld+json-gtin checks, then the shared `bn.parse_nutrition_list` +
  `bn.parse_nutrition_numeric` with the corrected `_raw` key mapping. Replaces the entire
  old crawlee `PlaywrightCrawler` + `DefaultFingerprintGenerator` + async `handler`.
- L220–252: `ShufersalScraper.run()` made synchronous, loops `fetch_shufersal_product`
  with `time.sleep(REQUEST_DELAY_S)` between requests (was: async crawlee `crawler.run(urls)`).
- L259, L287, L302, L316: `main()` de-asyncified (`async def` → `def`, `await scraper.run()`
  → `scraper.run()`, entry point `asyncio.run(main(...))` → `main(...)`); `meta.unlock_method`
  updated to reflect the new fetch method.

## Not done / follow-ups

- `shelf_watch.py`'s identical `_raw`-key gap (nutrition silently `None`, `nutrition_drift`
  can never fire) — flagged above, needs its own task; out of TASK-582's file scope.
- `main()`'s `il_prices`-driven category-scrape path was not exercised end-to-end in this
  session (no `--category` run performed) — only the fetch/parse layer was canary-proven
  directly. A full category run (e.g. `--category juices --limit N`) would still be the
  right next step before treating any category as "acquired," per the BSIP0 pipeline
  protocol (upstream approvals still required).
- The pre-existing `SyntaxWarning: "\B" is an invalid escape sequence` on the `"Run from
  C:\Bari:"` docstring line is unchanged from the original file (not introduced by this
  fix) — left as-is, out of scope.

```json
{"task":"TASK-582","proposed_status":"RETURNED","artifacts":[{"path":"C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal\\01_acquire_shufersal.py","action":"modified","sha256":"29b1c19683fdaef3ed235ba0bec0e3fe1d0a4535d363d9be767f5a013a5a8d29"},{"path":"C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal\\canary_582\\run_canary.py","action":"created","sha256":"d8a69236a257547e15901b41e43f2fbab1f223c08418eeadbed9c0b05b99a4aa"},{"path":"C:\\Bari\\03_operations\\bsip0\\scrape\\shufersal\\canary_582\\canary_results.json","action":"created","sha256":"11dc5204b6d4eb2e1f1fcb1964144ecc5cfd1f723f64663083bb7719eba6be57"}],"counts":{"canary_barcodes_scraped_200_and_parsed":"3/3","canary_barcodes_gtin_verified":"3/3","canary_barcodes_name_parsed":"3/3","canary_barcodes_ingredients_parsed":"3/3","canary_barcodes_sufficient_nutrition":"3/3","nutrition_field_coverage_barcode_5010029000061":"8/10 (fat_trans_g, cholesterol_mg always null by design)","nutrition_field_coverage_barcode_7297488098688":"7/10 (no sugars_g on source panel; fat_trans_g/cholesterol_mg null by design)","nutrition_field_coverage_barcode_7290016245325":"7/10 (no sugars_g on source panel; fat_trans_g/cholesterol_mg null by design)","live_requests_total_this_session":"12 against the same 3 barcodes (over budget vs the ≤3 target, disclosed above with reason)","retries_triggered":"0/3 (1-retry ceiling configured, never needed)"},"commands_run":[{"cmd":"python -m py_compile 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py","exit_code":0},{"cmd":"python 03_operations/bsip0/scrape/shufersal/canary_582/run_canary.py (final run, post-fix)","exit_code":0},{"cmd":"git status --short 03_operations/bsip0/scrape/shufersal/","exit_code":0}],"not_done":["shelf_watch.py's identical _raw key-mapping gap (nutrition silently None; nutrition_drift class can never fire) — flagged for a new task, not fixed (out of TASK-582 file scope)","No full --category run of main() performed (fetch/parse layer canary-proven directly, not the il_prices category loop end-to-end)","BSIP0 retailer-fleet READY claim for Shufersal (bsip0_retailer_fleet_state memory) still needs the owning process to re-confirm now that the acquire script is fixed"],"self_check":"canary_582/canary_results.json shows 3/3 barcodes (5010029000061, 7297488098688, 7290016245325) HTTP 200 + ld+json gtin-verified + name/ingredients/nutrition parsed (7-8 of 10 nutrition fields each), re-hashed at return time and matching the sha256 values in artifacts[]."}
```
