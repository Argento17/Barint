# TASK-602 Batch 3 — chocolate (bars + tablets) re-scrape (data-agent, 2026-07-11)

## SPEC-CONFLICT FLAG (read first): chocolate was NOT actually a blind shelf

The dispatch described bread + chocolate as "currently-blind shelves." Bread was
genuinely 0/23 (confirmed against the manifest *before* this batch touched
anything — see `task602_batch3_bread.md`). **Chocolate was not.** Before this
batch ran a single request, the capture manifest (rebuilt fresh at the start of
this session) already showed:

| Shelf | Manifest state BEFORE this batch (git HEAD at batch start) |
|---|---|
| chocolate_bars_frontend_v1 | **23/23 already canonical** |
| chocolate_tablets_frontend_v1 | **33/35 already canonical** (2 gaps) |

Root cause traced: both `build_manifest.py` and `build_census.py` were only
authored/ported in the TASK-602 milk pilot (commit `24ed81f8`) — **after** the
committed TASK-601 census (commit `ee6f64d8`, which reported chocolate at 0/23 and
0/35). TASK-601's original census used different, now-superseded tooling. The
underlying capture data itself is much older: `02_products/chocolate/bsip0_outputs/
choc_bsip0_raw_20260621T093256.json`, a full Shufersal chocolate scrape from
TASK-362 ("bars rework foundation", 2026-06-21) — three weeks before this task and
long before TASK-601 ran. The June-21 file was already committed to git; the
current (batch-2-ported) manifest tooling correctly indexes it; the TASK-601-era
tooling apparently did not (or ran before the file existed in its indexed form).

**Implication for the rest of TASK-602's planned fan-out:** the "0/N blind shelf"
list drawn from the committed TASK-601 census may be stale for OTHER shelves too,
not just chocolate. Recommend re-running `build_census.py` against the CURRENT
manifest tooling (already done here) before dispatching further batches, so no
future batch re-scrapes a shelf that already has usable captures sitting
uncounted. Flagging to Product/orchestrator rather than silently treating
chocolate as net-new work.

**What this batch actually did about it:** rather than skip chocolate outright (the
existing June-21 capture already covers 23/35 with no visible quality issue) or
blindly trust 3-week-old data as "the very best baseline" (owner's actual
instruction), this batch ran a **fresh, live re-scrape of all 58 chocolate products
today** — both to fill the 2 genuine tablets gaps and to get a current-dated
baseline, then diffed the fresh capture against BOTH (a) the served/published JSON
and (b) the old June-21 capture, to check for drift. See below — no drift, no
material discrepancy either way, so this was a confirmatory pass, not a rescue.

## Coverage (before -> after, this batch's numbers; the "before" column already
reflects the pre-existing June-21 captures, not zero)

| Shelf | Before (already-canonical, June-21) | After this batch |
|---|---:|---:|
| chocolate_bars_frontend_v1 | 23/23 | **23/23** (fresh re-confirm, same coverage) |
| chocolate_tablets_frontend_v1 | 33/35 | **35/35** (2 genuine gaps filled) |

0 NOT_FOUND on either shelf. All 58 products resolved via Shufersal alone (no
Tiv Taam/Hazi Hinam fallback needed) — including the 4 chocolate_bars short-code
served barcodes (`72991008`, `72917329`, `72917367`, `72918388`), which resolve
exactly the same way bread's short codes did: Shufersal's own `p/p_{code}` URL and
`ld+json` gtin match the served value exactly, name-verified. Same benign
"genuine Shufersal-internal SKU" finding as bread, not the yogurt-drink
truncation-corruption pattern. Recorded per-product in each shelf's
`*_rescrape_final.json` `barcode_reconciliation` field; 0 true barcode
reconciliations (served-truncated -> true-GTIN-discovered-elsewhere) were needed
on either chocolate shelf — every served barcode, short or long, already resolves
directly.

## Verify: captured vs published (TASK-595 thresholds)

**chocolate_bars** (23/23 evidence-backed): disposition **FULLY_MATCH 23/23**, zero
MATERIAL, zero ROUNDING, zero FIELD_GAP on energyKcal/protein/sugar/fat/sodium (all
n=23, all deltas 0.0, stdev 0.0). Fiber: n=4 comparable (both sides present, MATCH
4/4); the other 19 products have fiber null on BOTH the live panel and the
published JSON (no discrepancy, just absent data both sides — most chocolate
bars/wafers don't carry a fiber line).

**chocolate_tablets** (35/35 evidence-backed): disposition **FULLY_MATCH 35/35**,
zero MATERIAL, zero ROUNDING, zero FIELD_GAP on energyKcal/protein/sugar/fat/sodium
(all n=35, all deltas 0.0, stdev 0.0). Fiber: n=24 comparable (MATCH 24/24); 11
products have fiber null both sides.

**No TRIPWIRE-1 on either chocolate shelf** — this is the cleanest result of the
TASK-602 batches so far (milk/juices/bread all surfaced at least one real finding;
chocolate's published data matches the live label exactly on every comparable
field).

## Old (2026-06-21) vs new (2026-07-11) capture stability check

Cross-diffed today's fresh capture against the pre-existing June-21 capture for
every matched barcode (146 barcode-keyed objects available in the old file). **Zero
products showed a delta >0.15g/2mg-kcal on any field** — the 3-week-old capture and
today's are stable/identical within rounding on every shared field, for both
shelves. This corroborates that chocolate (shelf-stable, non-perishable) genuinely
does not need frequent re-scraping, unlike bread (which showed the fat-placeholder
issue) — a useful signal for future re-scrape cadence planning, not acted on here.

## Field-coverage (scrape side, this batch's fresh captures)

chocolate_bars: 23/23 have `energy_kcal`, `fat_g`, `fat_saturated_g`, `sodium_mg`,
`carbohydrates_g`, `sugars_g`, `protein_g`; 4/23 have `dietary_fiber_g` (rest
genuinely absent from the label). 23/23 non-empty `ingredients_raw`.

chocolate_tablets: 35/35 have `energy_kcal`, `fat_g`, `fat_saturated_g`,
`sodium_mg`, `carbohydrates_g`, `sugars_g`, `protein_g`; 24/35 have
`dietary_fiber_g`. 35/35 non-empty `ingredients_raw`.

## No published-JSON changes

`git status` confirms zero diff on
`bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json` and
`chocolate_tablets_frontend_v1.json`. Only new files under
`02_products/chocolate/bsip0_outputs/task602_chocolate_bars_rescrape_20260711/` and
`task602_chocolate_tablets_rescrape_20260711/`, plus the in-place manifest/census
refresh.
