# TASK-602 return — milk shelf full-traceability re-scrape pilot (Data Agent)

## Summary

Milk-shelf pilot for the corpus-wide re-scrape loop. Coverage moved from 0/18 to
17/18 canonical captures (18/18 attempted, 1 genuine NOT_FOUND). Verify step against
published `expansion.nutrition` found the loop is essentially trustworthy on
energy/sodium/sugar/protein (14/15 evidence-backed products FULLY_MATCH) but surfaced
one live-verified MATERIAL discrepancy (TRIPWIRE-1, below — surfaced, not acted on)
and one shelf-wide field-coverage gap (fat/carbs published-null on 15/15 evidence-backed
products despite being live-scrapable on all 15). No published JSON, score, or grade
was changed. Full narrative: `03_operations/reports/task602_milk_pilot.md`.

## Spec-conflict flags (raised before/during build, per Spec-Conflict Duty)

1. `03_operations/bsip0/manifest/{build_manifest.py,build_census.py,replay_harness.py,
   capture_manifest.json,replay_baseline.jsonl}` did not exist on branch `task506` (this
   branch forked before TASK-601's actual manifest tooling landed on `origin/master` at
   `f6c5206d`; only the census-closure commit was cherry-picked onto `task506`, not the
   tooling). Ported verbatim from `origin/master` (verified pure-addition diff first) so
   the task's own required commands would run. Compliant alternative to silently failing
   at step 4.
2. The brief states all 18 milk barcodes are Israeli 7290 GTINs. 5/18 are not (3x GS1-541
   Belgium, 2x GS1-800 Italy) — legitimate import barcodes, not an OFF violation (verified:
   all 5 scrape cleanly from the live Israeli Shufersal storefront under that exact
   barcode). Flagged, proceeded (data contradicted the brief's premise but not the task's
   intent).

## TRIPWIRE-1 (surfaced per task instruction — NOT acted on)

`8000215204554` (rice-coconut drink, score 48.1/D): published protein 0.4g/100ml vs a
fresh, unambiguous live Shufersal read of the same barcode/URL showing the "חלבונים"
row = `0` g. Delta 0.4g > the 0.15g MATERIAL threshold (TASK-595 buckets). The 0.4g
figure is quoted verbatim 3x in already-shipped consumer copy as the D-grade's stated
reason. No score/grade/JSON change made. Owning agents (Nutrition/Product) should
confirm the correct value before any correction.

## Field-coverage finding (not a tripwire — a coverage gap, flagged per Field-Coverage
Duty)

fat and carbs are published `null` on 15/15 evidence-backed milk products despite being
present on 15/15 live pages checked (saturated fat 9/15, fiber 8/15, sugar 4/15, sodium
2/15 similarly gapped). Shelf-wide BSIP1 enrichment gap, not a source-availability
problem. Recommend a follow-up re-enrichment task; not executed here (out of this
pilot's "no changes" scope).

## not_done

- Barcode `7290119385560` (Alpro soy barista 500ml) remains NOT_FOUND — checked
  Shufersal (404), Hazi Hinam dairy subcategory (no match), Tiv Taam 40-result
  "בריסטה" search (no barcode match). Did not attempt Yohananof (raw_store
  Playwright discovery scraper) or Victory — time-boxed for a pilot; a real fan-out
  pass would try the full fleet.
- `replay_baseline.jsonl` / `replay_harness.py` were NOT re-run against the rebuilt
  manifest (task step 4 named `build_manifest.py` + census explicitly; replay refresh
  was not requested and is now stale relative to the new 2456-record manifest —
  flagging so it isn't mistaken for current).
- Did not simulate a BSIP2 score delta for the TRIPWIRE-1 product — requires the
  scoring engine/weights, Nutrition Agent territory, explicitly out of scope
  ("do not act").
- Did not fix the `_PER_100G_MARKERS` per-100ml parser gap found on `7290014760141` —
  shared module, affects every retailer scraper, flagged as a follow-up only.

## self_check

Acceptance test (from the dispatch): "milk coverage moves from 0/18 toward 18/18
(minus any honest NOT_FOUND); state the exact new number." Observed: **17/18**
(1 genuine NOT_FOUND: `7290119385560`), independently re-derived twice — once via
`build_census.py`'s printed table, once by directly loading
`capture_manifest.json`'s canonical-GTIN set and checking each of the 18 served
`barcode` values against it in a separate script. Both give 17/18. PASS.

```json
{
  "task": "TASK-602",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/milk_rescrape_captures.json", "action": "created", "sha256": "72459f392f059e03571a236f66b7b255cd73a25f4356a8b6b471b1b03df2e8d1"},
    {"path": "02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/hazi_hinam_7290000051352.json", "action": "created", "sha256": "e2d0742f6366b13728d99af65c8ad0252d3f8f5bbb727229dff276576e79f201"},
    {"path": "02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/tivtaam_lookup_results.json", "action": "created", "sha256": "5bea0ee4b8790613f2174074ff192a63a0ac0b643682032b0aa08d31eecbdfa3"},
    {"path": "02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/milk_rescrape_final.json", "action": "created", "sha256": "987f7a58af713f8d165a86392943f0a03266c102da21bcfdb877fcb605cba03b"},
    {"path": "02_products/milk_and_alternatives/bsip0_outputs/task602_milk_rescrape_20260711/milk_rescrape_diff.json", "action": "created", "sha256": "3f5b797617662b32943b146f72a7f26b382e810d07dbf39d3e6eba80a992b2db"},
    {"path": "03_operations/bsip0/manifest/build_manifest.py", "action": "created", "sha256": "f9d9595e9e262ce89cd185905a004a91b9d957a0387c6cafa7d2c3f0328588c8"},
    {"path": "03_operations/bsip0/manifest/build_census.py", "action": "created", "sha256": "787516a24b814b4046290336b4ab140520259b072b5c63a31183fbaebd4b3334"},
    {"path": "03_operations/bsip0/manifest/replay_harness.py", "action": "created", "sha256": "19d95f4c14e2a8c80ebd07ed98e086871baad22207b6cf74659cc6bd35ace9a6"},
    {"path": "03_operations/bsip0/manifest/capture_manifest.json", "action": "created", "sha256": "fcf40ed0630830406d2b4a77e6826af0c28dedc1ffc95cf628d660b9fdbd3ddd"},
    {"path": "03_operations/bsip0/manifest/replay_baseline.jsonl", "action": "created", "sha256": "b896d77547a5c8a330b1e18d79002e911e6fe3a042ded61402a63147cc830602"},
    {"path": "03_operations/reports/task601_bsip0_census.md", "action": "modified", "sha256": "0b67ae0d8fa9814d50c027606b45b5ae87f1f4ae774ee988035486c9d1407645"},
    {"path": "03_operations/reports/task602_milk_pilot.md", "action": "created", "sha256": "77e60bdd9e98225389ab459dffc3ea82fcbe9e78bee4020a67654fdd003c0f3e"}
  ],
  "counts": {
    "milk_barcodes_scraped_ok": "17/18 (some retailer returned identity; source: milk_rescrape_final.json status field)",
    "milk_barcodes_usable_nutrition_panel": "16/18 (nutrition_raw_source.rows non-empty; source: milk_rescrape_final.json)",
    "milk_barcodes_not_found_anywhere": "1/18 (7290119385560; source: milk_rescrape_final.json)",
    "milk_manifest_coverage_before": "0/18 (source: TASK-601 closed census, git log ee6f64d8)",
    "milk_manifest_coverage_after": "17/18 (source: build_census.py stdout table AND independent recheck against capture_manifest.json canonical-GTIN set)",
    "evidence_backed_diff_comparisons": "15/18 (excludes 2 no-usable-panel + 1 not-found; source: milk_rescrape_diff.json)",
    "diff_disposition_FULLY_MATCH": "14/15 (source: milk_rescrape_diff.json)",
    "diff_disposition_MATERIAL_PRODUCT": "1/15 (barcode 8000215204554; source: milk_rescrape_diff.json)",
    "diff_disposition_NO_COMPARABLE_FIELDS": "2/18 (7290000051352, 7290014760141; source: milk_rescrape_diff.json)",
    "diff_disposition_NO_EVIDENCE": "1/18 (7290119385560; source: milk_rescrape_diff.json)",
    "field_match_energyKcal": "15/15 MATCH (source: milk_rescrape_diff.json, comparable-both-sides only)",
    "field_match_sodium": "13/13 MATCH (source: milk_rescrape_diff.json, comparable-both-sides only)",
    "field_match_sugar": "7/7 MATCH (source: milk_rescrape_diff.json, comparable-both-sides only)",
    "field_match_protein": "14/15 MATCH, 1/15 MATERIAL (source: milk_rescrape_diff.json)",
    "field_gap_fat_published_null_capture_has_value": "15/15 (source: milk_rescrape_diff.json)",
    "field_gap_carbs_published_null_capture_has_value": "15/15 (source: milk_rescrape_diff.json)",
    "field_match_energyKcal_delta_dist": "n=15, all deltas=0.0 (min=0.0 max=0.0 median=0.0 stdev=0.0 most_common=0.0x15/15); source: milk_rescrape_diff.json",
    "field_match_sodium_delta_dist": "n=13, all deltas=0.0 (min=0.0 max=0.0 median=0.0 stdev=0.0 most_common=0.0x13/13); source: milk_rescrape_diff.json",
    "field_gap_fat_captured_value_dist": "n=15, min=1.0g max=4.0g median=2.0g stdev=0.943g most_common=3.0g(x3); source: milk_rescrape_diff.json",
    "field_gap_carbs_captured_value_dist": "n=15, min=0.0g max=11.0g median=5.1g stdev=3.095g most_common=4.9g(x3); source: milk_rescrape_diff.json",
    "corpus_wide_manifest_total_before": "893 (source: TASK-601 closed census)",
    "corpus_wide_manifest_total_after": "2456 (source: build_manifest.py stdout, this branch's current tree)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip0/manifest/build_manifest.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/manifest/build_census.py", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_milk_rescrape.py (Shufersal-first, 18 barcodes)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_hazi_hinam_lookup.py (dairy subcategory scan)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_hazi_hinam_scrape_found.py (GS1 detail for item 145489)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_tivtaam_lookup.py (2 remaining barcodes)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_consolidate.py (merge fallback chain -> milk_rescrape_final.json)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_diff.py (verify captured vs published, TASK-595 thresholds)", "exit_code": 0}
  ],
  "not_done": [
    "7290119385560 remains NOT_FOUND (Yohananof/Victory not attempted -- time-boxed pilot)",
    "replay_baseline.jsonl/replay_harness.py not re-run against the new manifest (not requested by this task's step 4; now stale)",
    "No BSIP2 score-delta simulation for the TRIPWIRE-1 product (Nutrition Agent territory)",
    "_PER_100G_MARKERS per-100ml parser gap (found on 7290014760141) flagged, not fixed (shared module, out of scope)"
  ],
  "self_check": "Acceptance test: milk coverage 0/18 -> toward 18/18 minus honest NOT_FOUND, exact number stated. Observed 17/18, cross-verified two independent ways (build_census.py output vs direct capture_manifest.json canonical-GTIN check). PASS."
}
```
