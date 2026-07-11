# TASK-602 batch-2 return — juices + yogurt-drinkable re-scrape (Data Agent)

## Summary

Same loop as the milk pilot, run on juices (17 products) and yogurt-drinkable (17
products), both 0/17 captured before this run. Coverage: juices 0/17 -> **14/17**
(3 genuine NOT_FOUND); yogurt-drinkable 0/17 -> **17/17**. No published JSON, score,
or grade changed. Full narrative: `03_operations/reports/task602_batch2.md`.

## Major finding: truncated barcodes (yogurt-drinkable, 3/17)

Served `barcode` values `58030`, `4068035`, `55336` are exact digit-suffixes of the
true GTINs `7290000058030`, `7290004068035`, `7290000055336` (confirmed by locating
each product BY NAME on Hazi Hinam/Tiv Taam, then comparing the discovered true GTIN's
suffix against the served value). Not a Shufersal-availability issue — the served value
was never a resolvable barcode. **Recommend checking the other 380 no-capture products
for the same short-numeric-string pattern before further fan-out** — this could explain
some "not found" results elsewhere as false negatives.

## Two extraction bugs found in the verify step — corrected before reporting, one is a
LIVE production-pipeline bug (not just this pilot's script)

1. Tiv Taam sodium (juices `7290006822192`): my ad-hoc extraction didn't append the
   `מג` unit marker before `parse_sodium_mg`, so 5mg was mis-multiplied to 5000mg — a
   false MATERIAL flag traced to my own script, corrected (real value 5mg = MATCH).
2. Hazi Hinam sugar (yogurt-drink `4068035`): `bn.classify_nutr_label()` in
   `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` has no exclusion for a
   `"כפיות סוכר"` (teaspoon-count) row and matches it to `field="sugar"` same as the
   real gram row; first-value-wins picked the teaspoon row (0.75) over the gram row
   (3.3, matches published). **This is the exact code path in
   `03_operations/bsip0/scrape/hazi_hinam/acquire_hazi_hinam.py::scrape_item_panel`** —
   a real, already-shipped extraction bug, not unique to my scratch script. Flagged as
   a follow-up (add a teaspoon-row exclusion to `classify_nutr_label`, mirror the
   existing of-which/fat exclusion) — not fixed here (shared module, needs its own
   corpus-wide verification pass). Not fixed in this task's scope.

Both corrections are documented inline in the retention JSON (`extraction_bug_fixed`
field on each affected record) for traceability.

## No TRIPWIRE-1 in this batch

After correcting the two extraction bugs above, both shelves come back 100%
FULLY_MATCH on every evidence-backed product with zero MATERIAL discrepancies. No
copy-cited numeric claim was found to differ from a live label (checked per dispatch
instruction #6 — nothing survived the correction pass to check against).

## not_done

- 3 juice barcodes remain NOT_FOUND (`7290008690713`, `7290001247891`,
  `7290019056737`) — checked Shufersal + Tiv Taam only; Hazi Hinam has no juice
  category discovered in this pass (dairy-category nav only), Yohananof/Victory not
  attempted — time-boxed batch.
- Did not fix the `classify_nutr_label` teaspoon-row bug or re-verify other
  already-committed Hazi Hinam captures for the same corruption — flagged as a
  follow-up task, Nutrition/Product scoping call on priority.
- Did not check the other 380 no-capture products for the truncated-barcode pattern —
  recommended as a pre-fan-out step, not executed here.
- `replay_baseline.jsonl`/`replay_harness.py` not re-run against the newest manifest
  (same as the milk pilot; not requested).

## self_check

Acceptance test (same as milk pilot, applied per-shelf): coverage moves from 0/N
toward N/N minus honest NOT_FOUND, exact number stated. Observed: juices 14/17,
yogurt-drinkable 17/17 — both independently re-derived two ways (`build_census.py`
output vs direct `capture_manifest.json` canonical-GTIN check against each shelf's
served `barcode` field). PASS both shelves.

```json
{
  "task": "TASK-602",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/juices/bsip0_outputs/task602_juices_rescrape_20260711/juices_rescrape_shufersal_pass.json", "action": "created", "sha256": "94ad8b63d051a3e384c0373148e5195196c4af65ea28fc2f6f146c87d31b34a0"},
    {"path": "02_products/juices/bsip0_outputs/task602_juices_rescrape_20260711/tivtaam_fallback_results.json", "action": "created", "sha256": "40588e6b8329416859893611668e073c9dce2c2261a00ac73ab1aa3bddad8baf"},
    {"path": "02_products/juices/bsip0_outputs/task602_juices_rescrape_20260711/juices_rescrape_final.json", "action": "created", "sha256": "9e89466ceb1fd7560277f7196ed71fcace8915999f604d3c3d89c5c75141b62e"},
    {"path": "02_products/juices/bsip0_outputs/task602_juices_rescrape_20260711/juices_diff.json", "action": "created", "sha256": "9aa421166bbe6dddfbc816dedb1dbab5601c242d5f72fc87bc069d53925504ed"},
    {"path": "02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/yogurt_drinkable_rescrape_shufersal_pass.json", "action": "created", "sha256": "2d7f12a681e78ae9e0961972c5941c8b03ff57c7325f2d0caed5dc4d958adc12"},
    {"path": "02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/hazi_hinam_truncated_barcode_fixes.json", "action": "created", "sha256": "731bdd54284447441548dedad34dcb3dffc865bda7a7675c86af956b359230e6"},
    {"path": "02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/tivtaam_truncated_barcode_fix_55336.json", "action": "created", "sha256": "a8352ad8352f4090a93d065236f9efbb5385c6ec6b17f0a0ce1010f474cc9091"},
    {"path": "02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/yogurt_drinkable_rescrape_final.json", "action": "created", "sha256": "1a40556ce2bb67021d450fca7287005af6fc1434d16c9570a2caa63c1e82ce0b"},
    {"path": "02_products/yogurt_system/bsip0_outputs/task602_yogurtdrinks_rescrape_20260711/yogurt_drinkable_diff.json", "action": "created", "sha256": "0738948b5403c398e179017a5966399a8ae25308f8c762813fa796f353ee75a2"},
    {"path": "03_operations/bsip0/manifest/capture_manifest.json", "action": "modified", "sha256": "095b5e1fedd88c9758a60331e865958eedb6be91fdce1a86d4cecd2d43bc8f95"},
    {"path": "03_operations/reports/task601_bsip0_census.md", "action": "modified", "sha256": "770d4f8f192cb9b19d8503a7c72373fb9e2eaf5ad002d00c81e54766c892ed3f"},
    {"path": "03_operations/reports/task602_batch2.md", "action": "created", "sha256": "b9a37defe35d1738b1884d252d6985ae18f4286061b1965b0a84ec6b8ccbfc1c"}
  ],
  "counts": {
    "juices_coverage_before": "0/17 (source: TASK-601 census)",
    "juices_coverage_after": "14/17 (source: build_census.py stdout AND independent capture_manifest.json recheck)",
    "juices_not_found": "3/17 (7290008690713, 7290001247891, 7290019056737; source: juices_rescrape_final.json)",
    "yogurt_drinkable_coverage_before": "0/17 (source: TASK-601 census)",
    "yogurt_drinkable_coverage_after": "17/17 (source: build_census.py stdout AND independent capture_manifest.json recheck)",
    "yogurt_drinkable_truncated_barcodes_found": "3/17 (58030, 4068035, 55336; source: yogurt_drinkable_rescrape_final.json true_gtin_discovered field)",
    "yogurt_drinkable_usable_nutrition_panel": "16/17 (58030's hazi_hinam identity match has 0 nutrition rows; source: yogurt_drinkable_rescrape_final.json)",
    "juices_diff_disposition_FULLY_MATCH": "14/14 evidence-backed (source: juices_diff.json, post extraction-bug-fix)",
    "yogurt_drinkable_diff_disposition_FULLY_MATCH": "16/16 evidence-backed (source: yogurt_drinkable_diff.json, post extraction-bug-fix)",
    "juices_MATERIAL_discrepancies_after_bugfix": "0/14 (source: juices_diff.json)",
    "yogurt_drinkable_MATERIAL_discrepancies_after_bugfix": "0/16 (source: yogurt_drinkable_diff.json)",
    "extraction_bugs_found_and_corrected": "2/2 (Tiv Taam sodium mg-marker, Hazi Hinam sugar teaspoon-row; both documented inline in retention JSON via extraction_bug_fixed field)",
    "juices_energyKcal_delta_dist": "n=14, all deltas=0.0 (stdev=0.0, most_common=0.0x14/14); source: juices_diff.json",
    "juices_sugar_delta_dist": "n=12, all deltas=0.0 (stdev=0.0, most_common=0.0x12/12); source: juices_diff.json",
    "juices_carbs_gap_value_dist": "n=14, min=2.5g max=13.0g median=9.85g stdev=2.929g most_common=10.2g(x3); source: juices_diff.json",
    "yogurt_drinkable_energyKcal_delta_dist": "n=16, all deltas=0.0 (stdev=0.0, most_common=0.0x16/16); source: yogurt_drinkable_diff.json",
    "yogurt_drinkable_protein_delta_dist": "n=16, all deltas=0.0 (stdev=0.0, most_common=0.0x16/16); source: yogurt_drinkable_diff.json",
    "yogurt_drinkable_sodium_delta_dist": "n=16, all deltas=0.0 (stdev=0.0, most_common=0.0x16/16); source: yogurt_drinkable_diff.json",
    "yogurt_drinkable_carbs_gap_value_dist": "n=16, min=3.3g max=16.0g median=5.05g stdev=3.34g most_common=3.8g(x2); source: yogurt_drinkable_diff.json"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip0/manifest/build_manifest.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/manifest/build_census.py", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_batch2_rescrape.py (Shufersal-first, 34 barcodes, both shelves)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_batch2_fallback_tivtaam.py (10 remaining juice barcodes)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_batch2_consolidate.py (merge fallback chains + truncated-barcode discoveries)", "exit_code": 0},
    {"cmd": "python <scratchpad>/task602_batch2_diff.py (verify captured vs published, TASK-595 thresholds; re-run after extraction-bug fixes)", "exit_code": 0}
  ],
  "not_done": [
    "3 juice barcodes remain NOT_FOUND (Hazi Hinam has no discovered juice category; Yohananof/Victory not attempted -- time-boxed batch)",
    "classify_nutr_label teaspoon-row bug (hazi_hinam) flagged, not fixed -- shared module, needs corpus-wide re-verification before any fix",
    "Did not check the other 380 no-capture products for the truncated-barcode pattern found here -- recommended as a pre-fan-out step",
    "replay_baseline.jsonl/replay_harness.py not re-run (consistent with the milk pilot; not requested)"
  ],
  "self_check": "Acceptance test per shelf: coverage 0/N -> toward N/N minus honest NOT_FOUND, exact number stated, cross-verified two ways. Observed juices 14/17, yogurt-drinkable 17/17. PASS both."
}
```
