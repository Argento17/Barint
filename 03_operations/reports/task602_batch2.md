# TASK-602 Batch 2 — juices + yogurt-drinks re-scrape (data-agent, 2026-07-11)

Same loop as the milk pilot (`03_operations/reports/task602_milk_pilot.md`), applied to
the next two fully-blind shelves: juices (17 products) and yogurt-drinkable (17
products), both 0 captured before this run.

## Coverage (before -> after)

| Shelf | Before | After |
|---|---:|---:|
| juices_frontend_v3 | 0/17 | **14/17** |
| yogurt_drinkable_frontend_v1 | 0/17 | **17/17** |

Both independently re-derived twice: once via `build_census.py`'s printed table, once by
loading `capture_manifest.json`'s canonical-GTIN set directly and checking each served
product's own `barcode` field against it.

Not-found (juices, 3/17, checked Shufersal + Tiv Taam): `7290008690713` (מיץ חמוציות),
`7290001247891` (נקטר אפרסקים), `7290019056737` (מיץ אשכולית). Genuine misses — not
invented, not OFF-filled. Yogurt-drinkable: 0 not-found (see truncated-barcode finding
below for how the last 3 were resolved).

## Major finding: 3/17 yogurt-drink served barcodes are TRUNCATED, not real GTINs

The served `barcode` field for 3 yogurt-drink products is a short numeric string that
is not a resolvable retail barcode at all:

| Served `barcode` | True GTIN (discovered) | Product |
|---|---|---|
| `58030` | `7290000058030` | שטוזים משקה תות (8-pack strawberry yogurt drink) |
| `4068035` | `7290004068035` | איירן לשתיה (Eran drinkable yogurt) |
| `55336` | `7290000055336` | משקה יוגורט יופלה (Yoplait yogurt drink) |

In every case the served value is an **exact digit-suffix of the true 13-digit GTIN**
(`7290000058030` ends in `58030`; `7290004068035` ends in `4068035`;
`7290000055336` ends in `55336`) — a leading-digit truncation, not a typo or unrelated
number. This is why Shufersal's direct `p/p_{barcode}` lookup 404s on all 3: the served
value was never a real, addressable barcode. Confirmed by independently locating each
product BY NAME in Hazi Hinam's `יוגורט לשתיה` catalog subcategory (11582) and Tiv
Taam's search API, both of which return the full correct GTIN alongside the product
name/identity — the match was verified by name+brand, then the true-GTIN suffix
compared digit-for-digit against the served value (not the reverse).

This is a **corpus data-quality bug in the served frontend JSON's barcode field**
(likely from an earlier ingestion step that dropped leading digits — e.g. an
int/float cast that stripped a leading run of zeros, or a fixed-width truncation),
distinct from and worse than the milk pilot's "not all barcodes are 7290-prefixed"
finding (that was a legitimate-import-barcode false alarm; this is a real corruption).
**Recommend checking the other 380 no-capture products for the same
short-numeric-string pattern** (any served `barcode` under ~10 digits is suspect) before
the wider fan-out — this single pattern, if it recurs, would explain some of the
"not found" results across other blind shelves as false negatives (barcode literally
unresolvable, not "product genuinely absent from every retailer").

Retention (per served barcode, i.e. matching what the census/manifest join key
expects; the discovered true GTIN is recorded alongside every truncated record, not
substituted in place of the served value):
`02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/
yogurt_drinkable_rescrape_final.json`.

Note: `58030`/`7290000058030`'s Hazi Hinam identity match carries a GS1 record with
**zero nutrition rows** (ingredients-only, same pattern as the milk pilot's
`7290000051352`) — counts toward the 17/17 manifest-membership number but not toward
usable-nutrition coverage. 16/17 yogurt-drinks have a usable panel.

## Two extraction bugs found and corrected IN THIS PILOT'S OWN TOOLING (neither is a
real published-vs-live discrepancy — flagged per the two-sided-audit discipline
before either was mistaken for a TRIPWIRE)

**1. Tiv Taam sodium unit bug (juices, `7290006822192`, מיץ חמוציות דיאט).** Raw row:
`{"value":"5","unit":"מג","label":"נתרן (מג)"}` — 5 mg, matching published exactly. My
ad-hoc Tiv Taam extraction stored the bare value without appending the `מג` marker the
shared parser's `parse_nutrition_rows` requires before calling `parse_sodium_mg`, so
the "value>10 implies already-mg" heuristic mis-fired and multiplied 5mg x1000 ->
5000mg (also tripped the shared module's own >2000mg implausibility flag, which is
what caught it). **My pilot script's bug, not the published data's** — corrected to
5.0mg; the product is FULLY_MATCH once fixed.

**2. Hazi Hinam sugar teaspoon-row misclassification (yogurt-drink `4068035`, איירן
לשתיה) — LIVE BUG in the production pipeline, not just this pilot's script.** The Hazi
Hinam GS1 panel carries two sugar-shaped rows for this product: `"מתוכן כפיות סוכר"`
(teaspoon COUNT, Quantity=0.75, no unit) and `"סוכרים מתוך פחמימות"` (the real gram
value, Quantity=3.3, unit=גרם — matches published exactly). `bn.classify_nutr_label()`
(`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`) matches BOTH rows to
`field="sugar"` — its bare `"סוכר" in label` substring check has no teaspoon-row
exclusion. The existing teaspoon-exclusion (`teaspoon_marker_noop`, see that file's
`_YOHANANOF_LABEL_MAP` comment, TASK-515) lives ONLY in Yohananof's separate regex
label list, not in the generic `classify_nutr_label()` that Shufersal, Hazi Hinam, and
Tiv Taam all share. First-value-wins picked the teaspoon row here because the GS1 API
happened to return it before the gram row. **This exact extraction pattern
(`classify_nutr_label(label)` over `NutritionalValueDescription`, first-field-wins) is
the ACTUAL code in `03_operations/bsip0/scrape/hazi_hinam/acquire_hazi_hinam.py::
scrape_item_panel` — not unique to my scratch script.** Any already-committed Hazi
Hinam capture whose product carries a `"כפיות סוכר"` row before its real gram row has
the same silent corruption. **Flagged as a follow-up fix to the shared module (add a
teaspoon-row exclusion to `classify_nutr_label`, mirroring the existing "of-which"
sub-row exclusion for fat) — NOT fixed here** (shared module, needs its own
verification pass across whatever Hazi Hinam captures already exist in the corpus).
Corrected to 3.3g for this pilot's own reporting; the product is FULLY_MATCH once
fixed.

## Verify: captured vs published (after the two extraction-bug corrections above)

Thresholds per TASK-595 (MATCH <=0.05g/0.5mg-kcal, ROUNDING <=0.15g/2mg-kcal, MATERIAL
above; FIELD_GAP = one side null; NO_EVIDENCE = no usable panel).

**juices** (14 evidence-backed / 17 total): disposition FULLY_MATCH **14/14**, zero
MATERIAL, zero ROUNDING. Per-field (comparable-both-sides): energyKcal 14/14 MATCH
(deltas all 0.0, stdev 0.0), protein 13/13 MATCH, sugar 12/12 MATCH (deltas all 0.0,
stdev 0.0), fat 4/4 MATCH, sodium 4/4 MATCH.

**yogurt_drinkable** (16 evidence-backed / 17 total): disposition FULLY_MATCH **16/16**,
zero MATERIAL, zero ROUNDING. Per-field: energyKcal 16/16 MATCH (stdev 0.0), protein
16/16 MATCH (stdev 0.0), sugar 16/16 MATCH, fat 16/16 MATCH, sodium 16/16 MATCH (stdev
0.0), fiber 7/7 MATCH.

**No TRIPWIRE-1 in this batch** — both false-alarm MATERIAL flags traced to my own
extraction bugs (above), corrected, re-verified as FULLY_MATCH. No copy-cited numeric
claim was found to differ from a live label in this batch (checked per instruction
#6 — no MATERIAL survived the correction pass, so there was nothing left to cross-check
against shipped copy).

## Field-coverage finding (same pattern as milk — not a tripwire, a coverage gap)

**juices**: `carbs` published-null on 14/14 evidence-backed products despite being
live-capturable on all 14 (values 2.5-13.0g, median 9.85g) — identical pattern to milk.
`fat` and `sodium` are null on 9/14 (the rest match perfectly where both sides have a
value). `satFat` null on 13/14.

**yogurt_drinkable**: much better coverage than milk/juices — only `carbs` (16/16 gap,
values 3.3-16.0g, median 5.05g) and `satFat` (8/16 gap) are missing; energy, protein,
sugar, fat, sodium, and fiber are essentially fully populated and, where both sides
have a value, match at 100%.

Recommend the same milk-pilot follow-up (BSIP1 re-enrichment to backfill `carbs` across
the shelves that are missing it) extend to juices; yogurt-drinkable is a much smaller
gap (carbs + partial satFat only).

## No published-JSON changes

`git status` confirms zero diff on `bari-web/src/data/comparisons/juices_frontend_v3.json`
and `bari-web/src/data/comparisons/yogurt_drinkable_frontend_v1.json`. Only new files
under `02_products/juices/bsip0_outputs/` and
`02_products/yogurt_system/bsip0_outputs/`, plus the in-place manifest/census refresh.
