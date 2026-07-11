# TASK-602 Batch 5 — cakes_hard_cookies, cookies_coffee, crackers, protein_combined + juices mop-up (data-agent, 2026-07-11)

Ran in parallel with batch 3 (bread/chocolate, done) and batch 4 (cheese/hard_cheeses/yogurt-spoonable).
Scope: the blind (NO_CAPTURE) products on `cakes_hard_cookies_frontend_v1`, `cookies_coffee_frontend_v2`,
`crackers_frontend_v1`, `protein_combined_frontend_v2`, plus the `juices_frontend_v3` mop-up singletons.
`milk_frontend_v1` is SKIPPED — its 1 blind product was already fully investigated (Shufersal + Hazi Hinam +
Tiv Taam) by the dedicated milk agent and is a confirmed genuine NOT_FOUND; re-attempting would be duplicate
work. `bread_frontend_v3` is SKIPPED — confirmed legacy/unreferenced (see below).

## bread_frontend_v3 liveness check

`bread-comparison-page-data.ts` and `public-corpus-registry.ts` (the only two files under `bari-web/src`
that reference either bread frontend file) both import **only** `bread_frontend_v4.json`. `bread_frontend_v3.json`
has zero live import references. Confirmed legacy/superseded — not scraped, per instruction.

## Coverage (blind -> scraped, self-scoped against `capture_manifest.json`)

| Shelf | Blind (census) | Scraped | Genuine NOT_FOUND |
|---|---:|---:|---:|
| cakes_hard_cookies_frontend_v1 | 7 | **2** | 5 |
| cookies_coffee_frontend_v2 | 21 | **16** | 5 |
| crackers_frontend_v1 | 19 | **19** | 0 |
| protein_combined_frontend_v2 | 17 | **17** | 0 |
| juices_frontend_v3 (mop-up) | 3 | 0 | 3 (re-confirmed) |
| **Total** | **67** | **54** | **13** |

Every NOT_FOUND was checked against three engines before being recorded as genuine: Shufersal direct-by-barcode
(`p/p_{barcode}`), Shufersal search (by barcode text, then by product name, checking every candidate's ld+json
gtin), and Tiv Taam's v2 products API (Playwright, same engine `acquire_tivtaam.py` uses). No OFF, no
substitution, no invented data — an unresolved barcode is recorded as NOT_FOUND, never silently dropped or
filled from another source.

**juices mop-up**: independently re-ran all 3 already-documented NOT_FOUND barcodes from batch 2
(`7290008690713`, `7290001247891`, `7290019056737`) through the same three-engine loop (Shufersal direct +
search + Tiv Taam). Same result — genuine misses, reconfirmed, no new coverage found. Batch 2's finding stands.

## Tooling bugs found and fixed IN THIS BATCH'S OWN SCRIPT (neither is a real published-vs-live discrepancy)

**1. Double `p_` prefix silently 404'd every search-fallback candidate.** Shufersal's search-listing
`data-product-code` attribute already carries a `P_` prefix (e.g. `P_6983787`), but my first draft's PDP-fetch
helper unconditionally prepended another `p_`, producing `p_p_6983787` (404 on every attempt). This masked real
coverage on the very first shelf run (cakes_hard_cookies initially showed 1/7 instead of 2/7). Fixed by stripping
any existing `p_`/`P_` prefix before re-adding it once.

**2. A loose name-prefix fallback produced a FALSE-POSITIVE product match — caught before being retained.**
An early version accepted the first search candidate whose name shared a 12-character prefix with the target
name and returned immediately. On this near-duplicate bakery shelf (many `עוגת הבית <flavor>` / `עוגות אישיות
<flavor>` SKUs), this matched served barcode `7290006983787` ("עוגת הבית שוקולד צ'יפס") to a **completely
different product** — gtin `7290106574793` ("עוגת הבית שוקו שוקוצ'יפס"), a different SKU under a different GS1
prefix range entirely — before ever reaching the correct candidate later in the results list. Per the
product-names-are-verbatim-strings rule, this is exactly the failure class that rule exists to prevent. Caught
by manual spot-check before any capture was retained; the script was rewritten to (a) collect ALL search
candidates from both queries first, (b) accept a match ONLY on a deterministic barcode relationship — exact
gtin equality, or the `729000+internal-PLU` suffix pattern below — **never** on name similarity alone, and (c)
any name-only-adjacent candidate is now recorded as an unretained `review_candidates_NOT_RETAINED` list, never
silently promoted to a match. Re-ran cakes_hard_cookies after the fix; the corrected result (2/7) is what's
reported above and is what's captured on disk.

**3. Comma-as-thousands-separator sodium misparse (crackers, `7290018790328`, קרקר מרובע מלוח) — a KNOWN,
already-flagged defect in the shared parser, not something new.** Raw label: `"1,200 מג"` (1,200 mg). The shared
`_to_float()` in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` normalises decimal commas
(`.replace(",", ".")`) before regex-extracting the number, which turns `"1,200"` into `"1.200"` -> parsed as
**1.2**, not 1200. This produced a false MATERIAL flag (served 1200 vs "captured" 1.2) that is entirely my
tooling's own artifact — the served value (1200 mg) is correct, matches the live label exactly once the comma
bug is accounted for (FULLY_MATCH). This is the same defect class the existing replay harness already tracks
under the `comma_ambiguous` flag (`03_operations/bsip0/manifest/replay_baseline.jsonl`: 37 rows already flagged
project-wide) — **not a new bug, but a live reproduction of it**, confirming the flag is real and not a
harness false-positive. Not fixed here (shared module, out of this task's scope) — flagged as a follow-up.

## MAJOR FINDING 1 — crackers: fat-placeholder pattern on 19/19 (100%) of scraped products (EV-026 signature)

Every single scraped cracker shows a served `fat` value that is a small constant, wildly below the live-scraped
value — the exact bread EV-026 signature this batch was told to watch for, but at **full-shelf prevalence**
rather than bread's partial one. Two distinct placeholder constants appear:

- **`0.25` g** on 16/19 products (live range 2.0–32.2 g/100g)
- **`3.5` g** on 3/19 products (live range 12.0–18.0 g/100g) — a second, less-common placeholder constant, same
  signature (three unrelated products — a rosemary thin cracker, a rustic thin cracker, a cream cracker — all
  showing the identical 3.5g value while their live fat ranges 12–18g)

| Barcode | Product | Served fat (g) | Live fat (g) |
|---|---|---:|---:|
| 96086000966 | קרקר כוסמין מלא ושומשום | 0.25 | 10.6 |
| 96086000577 | קרקר כוסמין אורגני | 0.25 | 3.0 |
| 7290013740823 | קרקר כוסמין טבעי | 0.25 | 19.0 |
| 7296073659945 | קרקר דק רוזמרין | 3.5 | 17.0 |
| 7296073134459 | קרקר פריך בסגנון שוודי | 0.25 | 2.0 |
| 7296073134442 | קרקר פריך עם קמח שיפון | 0.25 | 2.2 |
| 7290013740809 | קרקר כוסמין סלק | 0.25 | 16.2 |
| 7290112963918 | קרקר דק רוזמרין פיטנס | 0.25 | 15.6 |
| 7296073659952 | קרקר דק כפרי | 3.5 | 18.0 |
| 7290115205176 | קרקר דק כפרי פיטנס | 0.25 | 17.0 |
| 7290112968821 | קרקר דק פיטנס בטטה | 0.25 | 15.5 |
| 8434165658523 | קרקר קרם קרקר | 0.25 | 14.0 |
| 7296073398875 | קרם קרקר | 3.5 | 12.0 |
| 74252 | קרקר שומשום אסם | 0.25 | 16.5 |
| 7290013740083 | קרקר דגנים ללת"ס | 0.25 | 32.2 |
| 74375 | קרקר זהב אסם | 0.25 | 20.0 |
| 7290011489595 | קרקר טופז שומשום | 0.25 | 17.3 |
| 7290018790328 | קרקר מרובע מלוח | 0.25 | 18.0 |
| 5000396021202 | קרקר | 0.25 | 23.0 |

All 19 confirmed via direct Shufersal `p/p_{barcode}` fetch (no search/fallback ambiguity), per-100g basis
explicitly selected by the shared parser (`extract_nutrition_selection`, `selected_basis="per_100g"`), so this
is not a basis-mismatch artifact — it is a genuine served-vs-live fat discrepancy across the entire blind
cracker set. **TRIPWIRE-1 per the hard rules: recorded, NOT corrected, product scoring left untouched.**
Escalating to Nutrition Agent — crackers scored on a near-zero fat input for every one of these products would
materially understate their fat/energy-density profile (some are 30+ g fat/100g live, essentially a shortbread
fat level, scored as near-fat-free). If this pattern extends into the 34/53 already-canonical crackers (batch-5
only rescraped the 19 blind), the shelf's scores may need a full re-verification pass — flagging for Nutrition
Agent + Product Agent judgment, not deciding it myself.

## MAJOR FINDING 2 — cookies_coffee: 4 products show served nutrition ~5–6x LOWER than live, despite an
explicit "ל-100 גרם" (per 100g) serving-note claim on both sides — live-verified, TRIPWIRE-1

| Barcode | Product | Field | Served | Live | Ratio |
|---|---|---|---:|---:|---:|
| 7290122781359 | מיני עוגיות קלאסי 80 גרם | energyKcal | 93.0 | 465.0 | 5.00x |
| | | protein | 1.8 | 9.0 | 5.00x |
| | | fat | 3.6 | 18.0 | 5.00x |
| | | sugar | 4.6 | 22.8 | 4.96x |
| | | sodium | 55.0 | 275.0 | 5.00x |
| | | fiber | 1.1 | 5.5 | 5.00x |
| 7290000061245 | עוגיות שוקוצ'יפס ממולאות 220 ג | energyKcal | 97.0 | 527.0 | 5.43x |
| | | protein | 1.2 | 6.4 | 5.33x |
| | | fat | 5.2 | 28.2 | 5.42x |
| | | sugar | 6.2 | 34.0 | 5.48x |
| | | sodium | 31.0 | 170.0 | 5.48x |
| 7290118423904 | קראנץ שוקו וניל עוגיות 200 גרם | energyKcal | 94.0 | 554.0 | 5.89x |
| | | fat | 5.4 | 32.0 | 5.93x |
| | | sugar | 6.3 | 37.0 | 5.87x |
| | | sodium | 19.0 | 110.0 | 5.79x |
| 7290118422617 | קראנץ קרם וניל עוגיות 200 גרם | energyKcal | 92.0 | 539.0 | 5.86x |
| | | fat | 4.9 | 29.0 | 5.92x |
| | | sugar | 6.0 | 35.0 | 5.83x |
| | | sodium | 14.0 | 80.0 | 5.71x |

Ruled out as a basis-mismatch artifact of my own tooling: re-fetched all 4 pages directly and confirmed via
`bsip0_nutrition.extract_nutrition_selection()` that the live per-100g table is unambiguous
(`selected_basis="per_100g"`, `insufficient=False`) — this is the SAME per-100g panel the served corpus claims
(`expansion.servingNote = "ל-100 גרם"` on all 4). The live-captured values (465–554 kcal/100g, 18–32g fat/100g)
are the physically plausible range for this product type (cookies); the served values (92–97 kcal/100g,
3.6–5.4g fat/100g) are implausibly low for cookies — closer to a fruit or vegetable's energy density — and the
~5–6x ratio is suspiciously uniform across every field for a given product, consistent with a per-serving value
(roughly a 17–20g single-cookie serving) having been captured upstream and mislabeled as per-100g rather than
scaled. **Recorded, NOT corrected — TRIPWIRE-1. Escalating to Nutrition Agent: if these 4 products' published
scores were computed from the served (too-low) values, their macro profile is being understated across the
board, which would inflate their grade relative to reality.**

## Other MATERIAL discrepancies (not part of either pattern above)

**cookies_coffee, `7290013156006` (עוגיות מיני מרוקאיות)** — smaller, mixed deltas, most fields within a few
percent (energy 435 served vs 449 live, protein/fat/sugar/fiber all close), **except sodium: 91 mg served vs
22.8 mg live — a 4x discrepancy in the opposite direction** (served higher than live). Basis confirmed
unambiguous (`competing_table_count=1`, `selected_basis="per_100g"`); the live row read directly as `"22.8 מג"`.
Recorded as MATERIAL, not corrected — could be a genuine reformulation/label update since the served snapshot
was taken, or an unrelated capture-time error; not diagnosed further here (out of this task's scope to
root-cause).

## Barcode reconciliation — benign_retailer_sku vs true_truncation

| Shelf | benign_retailer_sku | true_truncation |
|---|---:|---:|
| cakes_hard_cookies_frontend_v1 | 2 | 0 |
| cookies_coffee_frontend_v2 | 16 | 0 |
| crackers_frontend_v1 | 19 | 0 |
| protein_combined_frontend_v2 | 17 | 0 |
| **Total** | **54** | **0** |

No true truncations found this batch (unlike batch 2's yogurt-drinkable finding). Two benign sub-patterns
observed among the `benign_retailer_sku` count:
- **`exact`** — direct `p/p_{barcode}` 200 hit, or a search-fallback candidate whose ld+json gtin exactly equals
  the served barcode (the large majority — 51/54).
- **`synthetic_729000_plu`** — served barcode is `"729000"` + a short (5–8 digit) Shufersal-internal PLU, and
  that short PLU IS the page's own `gtin13`/`sku` (not a separate real GS1 barcode) — observed on 3/54
  (`7290006983787`→PLU `6983787`; `7290000061245`→PLU `61245`; `7290000075143`→PLU `75143`). This is Shufersal's
  own convention for in-house/fresh bakery goods that never had a printed GS1 barcode, not a corpus data-quality
  bug — the served value correctly and consistently identifies the product.

## Field-coverage note (consistent with the milk/juices pattern from earlier batches)

`carbs` is served-null on every single scraped product across all 4 main shelves (0/54 coverage) despite being
live-capturable on all of them (crackers alone: 19/19 live values, 49.4–67g range). `satFat` is served-null on
cookies_coffee (0/15 comparable) and protein_combined (0/17) despite full live coverage. This is the same
BSIP1-enrichment gap flagged in the milk pilot and batch 2 — recommend the same follow-up (re-enrichment to
backfill `carbs`/`satFat` across these shelves), not something to fix in this task.

## Artifacts (all task-scoped, no shared manifest/census touched)

- `02_products/cakes_hard_cookies/bsip0_outputs/task602_cakes_hard_cookies_rescrape_20260711/cakes_hard_cookies_frontend_v1_rescrape_results.json`
- `02_products/cookies_coffee/bsip0_outputs/task602_cookies_coffee_rescrape_20260711/cookies_coffee_frontend_v2_rescrape_results.json`
- `02_products/crackers/bsip0_outputs/task602_crackers_rescrape_20260711/crackers_frontend_v1_rescrape_results.json`
- `02_products/snack_bars/bsip0_outputs/task602_protein_combined_rescrape_20260711/protein_combined_frontend_v2_rescrape_results.json`
- `02_products/juices/bsip0_outputs/task602_juices_batch5_mopup_20260711/juices_frontend_v3_rescrape_results.json`
- `03_operations/bsip0/scrape/_task602_batch5/rescrape_batch5.py` — the rescrape engine (shared across all 5
  shelves in this batch; documents both tooling bugs found/fixed above in its own docstrings/comments)

## No served-JSON changes

`git status` confirms zero diff on any `bari-web/src/data/comparisons/*.json` file. Only new files under
`02_products/*/bsip0_outputs/` and the new task-scoped scraper script. The shared `capture_manifest.json` /
`replay_baseline.jsonl` are untouched (concurrency rule — batch 4 runs at the same time; orchestrator does one
consolidated manifest rebuild after the wave).
