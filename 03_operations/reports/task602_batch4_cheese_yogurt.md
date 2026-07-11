# TASK-602 Batch 4 — cheese + yogurt-spoonable re-scrape (data-agent, 2026-07-11)

Ran concurrently with batch 3 (bread + chocolate). Scope: all served cheese
comparison files except any already fully captured, plus `yogurt_spoonable_frontend_v1`.
Did NOT touch `capture_manifest.json`, the shared census, or bread/chocolate.

## Shelves in scope and self-scope result (vs `capture_manifest.json` at run start)

| Shelf | Served products | Already covered (skipped) | Blind (scraped this run) |
|---|---:|---:|---:|
| `brined_cheeses_frontend_v2` | 36 | **36/36 — fully covered, SKIPPED entirely** | 0 |
| `cheese_frontend_v4` | 47 | 10 | 37 |
| `hard_cheeses_frontend_v4` | 31 | 0 | 31 |
| `yogurt_spoonable_frontend_v1` | 50 | 49 | 1 |

`brined_cheeses_frontend_v2` needed zero work per the dispatch's "except any already
fully captured" instruction — confirmed 36/36 served barcodes already have a
canonical capture in the manifest.

## Coverage (blind products only, before -> after this run)

| Shelf | Before | After |
|---|---:|---:|
| `cheese_frontend_v4` | 0/37 | **37/37** |
| `hard_cheeses_frontend_v4` | 0/31 | **29/31** |
| `yogurt_spoonable_frontend_v1` | 0/1 | **1/1** |

**2 genuine NOT_FOUND** (both `hard_cheeses_frontend_v4`, both `served_retailer:
yohananof`, both valid-length GTINs):
- `7290004122348` — פרוסות גבינת עמק מופחתת שומן 9% בד"צ 200 גרם
- `7290117265888` — גבינת גאודה מגורדת יוחננוף 400 גרם

Both were searched on Shufersal (name + brand-token variants, multiple candidate
fetches) and are genuinely absent from Shufersal's own catalog — they read as
Yohananof-exclusive private-label SKUs. Per retailer priority (Shufersal ->
Victory -> Yochananof -> Rami Levy) the next step is a direct Yohananof scrape,
which this batch's tooling only supports via a Playwright-driven, semi-interactive
discover/approve/scrape flow (`03_operations/bsip0/scrape/yohananof/`) — out of
scope for this pass given the live-network time budget; NOT_FOUND recorded rather
than guessed. Victory has no non-Playwright acquirer either. Flagging for the
orchestrator's follow-up rather than silently leaving these uncaptured without
a note.

## Barcode reconciliation — IMPORTANT: this is NOT the truncation pattern the
dispatch anticipated

20 of the 69 blind products carry a served `barcode` that is not a valid-length
GTIN (8/12/13/14 digits) — the "high-truncation shelf" signal the dispatch flagged.
For **every one of the 20**, resolving by verbatim name (and, where ambiguous by
name alone, by brand cross-check — see finding below) led back to **Shufersal's own
product page at that exact same short code** (`P_{code}`) — never to a longer/
different GTIN found elsewhere. Reading the product page's `ld+json`, Shufersal
itself has no `gtin13` for these SKUs; the short number IS the retailer's native
internal SKU identifier (same benign pattern batch 3 documented for bread's short
codes, `task602_batch3_bread.md`).

**Conclusion:** 0/20 truncated-looking barcodes resolved to a genuinely different,
longer true-GTIN. All 20 are Shufersal-native short codes with no GTIN13 exposed at
this source. Finding this would require cross-referencing Victory/Rami Levy/il_prices
catalogs (heavier, out of scope here) — flagging as a limitation, not overstating a
resolution that didn't happen. Full table (all 20 rows: served code, resolved code,
retailer, product name) is in each shelf's raw-capture JSON under `barcode
reconciliation`-equivalent fields (`resolved code == served code` for all 20).

## METHODOLOGY FINDING (self-caught before commit): name-only matching produced 2
false-positive product matches — brand cross-check is now mandatory

During resolution, two candidates matched on product name/percentage-tier alone but
carried the **wrong manufacturer brand**:
- `2868996` (served brand טרה/Tara, "קוטג' 5% שומן") — a name-overlap search first
  matched brand שטראוס/Strauss's identically-named "קוטג' 5% שומן" (different GTIN,
  different real nutrition panel).
- `56272` (served brand תנובה/Tnuva, "גבינה לבנה עם זיתים 5%" — white cheese *with
  olives*) — matched brand סקי/Ski's plain "גבינה לבנה 5%" (no olives; this is what
  produced the one spurious MATERIAL sodium delta seen mid-run, since resolved).

Root cause: several fat-tier variants (`קוטג' 5%`, `קוטג' 9%` etc.) are sold by
3+ manufacturers under visually identical Hebrew product names with no brand token
in the name string itself — name-token overlap alone cannot disambiguate. **Fix
applied and re-verified live before commit:** both served codes ARE directly
fetchable Shufersal SKU codes (`P_2868996`, `P_56272`) — a direct-code fetch (tried
first, ahead of any fuzzy search) returns the correct brand and product for both.
Every truncated-barcode entry in this batch was re-verified via direct-code-fetch
(not fuzzy match) before being written to the final capture files; the 2 false
matches were rejected and corrected, never shipped. Flagging this pattern for the
orchestrator in case other TASK-602 batches' resolvers rely on name-overlap alone
without a brand cross-check or a direct-code-first attempt.

## Verify: captured vs published (TASK-595 thresholds: MATCH <=0.05g/0.5kcal-mg,
ROUNDING <=0.15g/2kcal-mg, MATERIAL above; FIELD_GAP = one side null)

Disposition across all 67 resolved products: **FULLY_MATCH 64/67, MATERIAL_PRODUCT
3/67, ROUNDING_ONLY 0/67, NO_EVIDENCE 2/67** (the 2 NOT_FOUND above).

Per-field (comparable-both-sides, n = non-FIELD_GAP pairs):
- `energyKcal`: n=67, 65 MATCH / 1 ROUNDING / 1 MATERIAL, deltas -1.0..3.0, stdev=0.39
- `fat`: n=67, 67 MATCH / 0 ROUNDING / 0 MATERIAL, deltas 0.0..0.0, stdev=0.00
- `protein`: n=67, 66 MATCH / 0 ROUNDING / 1 MATERIAL, deltas -0.3..0.0, stdev=0.04
- `sodium`: n=67, 66 MATCH / 0 ROUNDING / 1 MATERIAL, deltas 0.0..30.0, stdev=3.64
- `sugar`: n=23, 22 MATCH / 0 ROUNDING / 1 MATERIAL, 44 FIELD_GAP (sugar not
  declared/published on most cheese SKUs — a coverage gap, not a tripwire)
- `fiber`: n=1, 1 MATCH, 66 FIELD_GAP (cheese/yogurt rarely declares fiber — genuine
  source-side absence, confirmed by full-page-text grep showing no "סיבים" row, not
  a parser miss)

**MATERIAL findings (3 products, 4 field instances) — small, isolated, NOT a
systemic pattern (unlike batch 3's bread fat-placeholder finding):**
- `7290114310918` קוטג' 5% (טרה): sodium served 320mg vs captured 350mg (delta 30mg,
  ~9%)
- `7290112342102` גבינה 5% בצל מקורמל (סימפוניה): protein 8.7 vs 8.4 (delta -0.3g);
  sugar 5.4 vs 5.1 (delta -0.3g)
- `3073781199918` גבינה חצי קשה 24% בייבי בל (yohananof): energyKcal 305 vs 308
  (delta 3 kcal)

Per hard rule #5/#7: recorded here and in each product's raw-capture entry, **NOT
corrected**. No published JSON, score, or grade was touched — `git diff --stat` on
all 4 served files (`cheese_frontend_v4.json`, `hard_cheeses_frontend_v4.json`,
`yogurt_spoonable_frontend_v1.json`, `brined_cheeses_frontend_v2.json`) is empty.
These 3 read as ordinary small label/measurement variance, not the order-of-magnitude
bread pattern — no Nutrition Agent escalation recommended, but included here per the
hard-rule requirement to record every MATERIAL finding.

## Parser findings

- No `insufficient`-basis selections and no `_integrity` flags (fat-overwrite /
  sodium-implausible signatures) across all 67 captures — `bsip0_nutrition.py`'s
  shared parser held up cleanly on every Shufersal page hit this batch.
- 6/67 captures have empty `ingredients_raw` (all `hard_cheeses_frontend_v4`:
  imported/specialty cheeses — Gouda Masdam Emmental, Gouda Gusto 30%, Grana Padano
  grated, Gouda pesto 32%, plain yellow cheese 32% x2). Confirmed genuine source-side
  absence, not a parser miss: full-page-text search for "רכיב" returns no match at
  all on these pages (the retailer simply never published an ingredient list for
  them online). Correctly NULL per the missing-data-discard rule — no re-sourcing
  attempted.
- Transient Shufersal SSL resets (`SSLEOFError`) occurred intermittently (~10-15% of
  direct-fetch calls) mid-run, self-recovering on retry in every case tested; not a
  parser defect, a live-network flake. Retried failures individually before final
  write; none left unresolved because of it.

## No published-JSON changes

`git status`/`git diff --stat` confirm zero diff on any of the 4 served comparison
files in scope. Only new files under:
- `02_products/cheese_spreads/bsip0_outputs/task602_cheese_frontend_v4_rescrape_20260711/`
- `02_products/hard_cheeses/bsip0_outputs/task602_hard_cheeses_rescrape_20260711/`
- `02_products/yogurt_system/bsip0_outputs/task602_yogurt_spoonable_rescrape_20260711/`
- this report.

No edit to `capture_manifest.json`, `build_census.py`, or any batch-3 (bread/
chocolate) path.
