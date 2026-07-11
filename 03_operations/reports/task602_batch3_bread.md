# TASK-602 Batch 3 — bread re-scrape (data-agent, 2026-07-11)

Same loop as milk/juices/yogurt-drinkable. Shelf: `bread_frontend_v4` (23 products,
0/23 captured before this run — confirmed genuinely blind via the pre-rebuild
manifest, unlike chocolate; see the separate premise-correction note in
`task602_batch3_chocolate.md`).

## Coverage (before -> after)

| Shelf | Before | After |
|---|---:|---:|
| bread_frontend_v4 | 0/23 | **23/23** |

0 NOT_FOUND. All 23 resolved via Shufersal alone (no Tiv Taam/Hazi Hinam fallback
needed).

## Barcode finding: 15/23 served barcodes are SHORT (<10 digit) codes, but this is
NOT the yogurt-drink truncation-corruption pattern — it is a distinct, benign finding

15 of bread's 23 served `barcode` values are short numeric strings (e.g. `3268429`,
`481203`, `2079033`) that are not valid-length GTINs. Unlike the yogurt-drinkable
batch (where the short value was a truncated *suffix* of a real, independently
discoverable 13-digit GTIN), every one of these 15 bread codes **resolves directly**
on Shufersal's own `p/p_{code}` URL: the page's `ld+json` `gtin` field equals the
exact served value, and the returned product name matches the served name in all 15
cases (verified name-for-name; one case, `7290016967074`, resolves to a
brand-qualified variant of the same name — "לחם אנג'ל חיטה מלאה" vs served "לחם חיטה
מלאה" — same product, brand-qualified page title).

**Conclusion: these are genuine Shufersal-internal SKU codes for fresh-bakery items**
(not centrally GS1-registered packaged goods), not a truncation bug. No barcode
reconciliation ("true GTIN discovered elsewhere") was needed or performed for bread —
the served value already is the correct, directly-addressable identifier. Recorded
per-product in `bread_rescrape_final.json`'s `barcode_reconciliation` field for the
record, distinguishing this class from the yogurt-drink corruption class.

## MAJOR FINDING (TRIPWIRE-1): systematic `fat` field discrepancy, 18/23 bread products —
**recorded, NOT corrected, escalating**

18 of 23 bread products show a MATERIAL fat discrepancy (TASK-595 thresholds:
MATCH <=0.05g, ROUNDING <=0.15g, MATERIAL above). The published `fat` value is
**exactly `0.25`g on 14/18 of these**, `0.5`g on 3/18, with the live Shufersal panel
showing real values from 1.0g to 9.1g (median ~2.7g) for the SAME products. All 18
affected products carry `"confidence": "partial"` / `"confidence_sub_reason":
"low_extraction"` in the served JSON — meaning the page already self-flags this data
as incomplete, but the specific constant-looking `0.25`/`0.5` values read as real
numbers on the page, not as visibly-missing data. The pattern (same constant across
totally unrelated bread formulations — whole wheat, rye, spelt, seeded, keto) is far
more consistent with a **null-to-placeholder fallback bug at an earlier
enrichment/ingestion step** than with 18 independent real-world label misreads.

One product (`bsip1_bread_7290016967074`, "לחם חיטה מלאה") shows MATERIAL drift on
**five** fields simultaneously (energyKcal -17, protein -1.5g, fat +3.75g, fiber
+0.8g, sodium -23mg) — broader than the isolated fat-only pattern seen in the other
17, worth a second look as a possibly-different root cause (stale panel / reformulated
product / brand-variant mismatch) rather than the same placeholder bug.

**Per hard rule #5/#7 and the dispatch's TRIPWIRE-1 instruction: recorded in
`bread_diff.json`, NOT corrected. No published JSON, score, or grade was touched.**
Escalating to Nutrition Agent + Product Agent — this is a corpus-wide bread-shelf
data-quality issue that plausibly affects live scores (fat is scored; understating it
at 0.25g vs a real 1-9g would inflate every affected product's fat sub-score).

## Field-coverage (scrape side)

23/23 have full `energy_kcal`, `fat_g`, `sodium_mg`, `carbohydrates_g`, `protein_g`;
22/23 have `dietary_fiber_g` and `sugars_g`; 16/23 have `fat_saturated_g`. 23/23 have
non-empty `ingredients_raw`.

## Verify: captured vs published (TASK-595 thresholds)

Disposition: **FULLY_MATCH 5/23, MATERIAL_PRODUCT 18/23** (all MATERIAL = the fat
finding above, plus the one 5-field product). Zero ROUNDING_ONLY. Zero NO_EVIDENCE.

Per-field (comparable-both-sides, n = non-FIELD_GAP pairs):
- `energyKcal`: n=23, 22 MATCH / 1 MATERIAL (the 5-field product), deltas range
  -17.0..0.0, stdev=3.47.
- `protein`: n=23, 22 MATCH / 1 MATERIAL, deltas -1.5..0.0, stdev=0.31.
- `fat`: n=23, 5 MATCH / 0 ROUNDING / **18 MATERIAL**, deltas 0.0..8.85, stdev=2.13.
- `fiber`: n=22, 21 MATCH / 1 MATERIAL, deltas 0.0..0.8, stdev=0.17.
- `sodium`: n=23, 22 MATCH / 1 MATERIAL, deltas -23.0..0.0, stdev=4.69.
- `sugar`: n=1 comparable (MATCH) / **21 FIELD_GAP** (published sugar is null on
  21/23 bread products despite being visible on some live panels only where the
  retailer exposed a sugar row — same "carbs/sugar gap" pattern flagged in the
  milk/juices pilots, not a tripwire, a coverage gap).

## No published-JSON changes

`git status` confirms zero diff on `bari-web/src/data/comparisons/bread_frontend_v4.json`.
Only new files under `02_products/bread/bsip0_outputs/task602_bread_rescrape_20260711/`,
plus the in-place manifest/census refresh.
