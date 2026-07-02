# P473 Contract — TASK-466 derived live_manifest (kill "categories outside the safety net")

**Worktree:** `C:\bari_wt_t466` (branch `feat/task466-live-manifest`)
**Status proposed:** RETURNED

## Summary

Built `03_operations/page_generator/live_manifest.py` — statically derives a single live-category manifest from `bari-web/src/lib/comparisons/registry/` plus each category's page-data JSON import chain. Committed `live_manifest.json` (7 categories, 0 gaps). Wired `conformance.py --all` to read its category/config stem list from the manifest (with `--categories` override). Added CI drift gate to `barint_ci.yml`.

## Manifest content (7/7 live registry categories)

| category_id | route | frontend_json | config_json | catalog |
|-------------|-------|---------------|-------------|---------|
| bread | /hashvaot/bread | bread_frontend_v4.json | bread.json | yes |
| breakfast-cereals | /hashvaot/breakfast-cereals | cereals_frontend_v2.json | cereals.json | yes |
| cheese | /hashvaot/cheese | cheese_frontend_v5.json | cheese.json | yes |
| crackers | /hashvaot/crackers | crackers_frontend_v1.json | crackers.json | yes |
| granola | /hashvaot/granola | granola_frontend_v2.json | granola.json | yes |
| hummus | /hashvaot/hummus | hummus_frontend_v5.json | hummus_shelfrel_002.json | yes |
| snacks | /hashvaot/snacks | snacks_frontend_v5.json | snacks.json | yes |

**Gaps:** none (7/7 categories fully resolved — no `gaps` field on any entry).
**Headline finding:** no previously-uncovered live comparison category discovered; manifest matches the 7-entry comparisons registry exactly. Catalog-only slugs (brined-cheeses, cakes, juices, etc.) correctly excluded — they have `public-corpus-registry.ts` entries but no `comparisonCategoryRegistry` route.

## Drift-check demonstration

**Clean check (exit 0):**
```
python 03_operations/page_generator/live_manifest.py --check
LIVE_MANIFEST CHECK: PASS
  WARN: orphan config (no live page): ... (10 pipeline configs)
```

**Synthetic drift (exit 1):**
```
python 03_operations/page_generator/live_manifest.py --check --simulate-drift
LIVE_MANIFEST CHECK: FAIL
  ERROR: DRIFT (simulate): committed manifest differs from fresh derivation
```

## Conformance category sets

| set | count | members |
|-----|------:|---------|
| **Before** (`--all` = every `configs/*.json` stem) | 18/18 | bread, brined_cheeses, cakes, cereals, cheese, chocolate_bars, chocolate_tablets, cookies_coffee, crackers, crackers_frontend_discards_v1, granola, hard_cheeses, hummus_shelfrel_002, juices, milk, protein_bars, snacks, snacks_task413_staging |
| **After** (`--all` = manifest-derived config stems) | 7/7 | bread, cereals, cheese, crackers, granola, hummus_shelfrel_002, snacks |

**Difference explained:** 11/18 old stems are pipeline configs for categories without a live comparisons-registry route (catalog-era or staging). Intentional narrowing — conformance `--all` now tracks frontend live pages only. crackers (TASK-433) was already in the old 18-stem set; no net-new live category surfaced.

**Conformance result on manifest set:** 5/7 conform, 2/7 non-conforming (pre-existing HARD-3 baseline drift: bread config→v3 vs page v4; cheese config→v4 vs page v5). Not introduced by this pass.

## Follow-up: rescore_all / spine_flip adoption

Both use `list_live_shelves()` → every `configs/*.json` stem (18 today). Adoption would require:
1. Import `live_manifest.manifest_config_stems()` (or shared helper) instead of globbing all configs.
2. Map manifest `config_json` paths to stems; skip categories with `gaps` (emit WARN).
3. Keep a `--categories` / `--all-configs` escape hatch for pipeline-only rescoring.
4. Update `spine_flip.py:303` rescore loop and `rescore_all.py` shelf enumeration (~10 lines each).
5. Re-run spine smoke + one flip dry-run to confirm 7-shelf rescore set.

## Gate outputs

| # | command | exit |
|---|---------|-----:|
| 1 | `python 03_operations/page_generator/live_manifest.py` | 0 |
| 2 | `python 03_operations/page_generator/live_manifest.py --check` | 0 |
| 3 | `python 03_operations/page_generator/live_manifest.py --check --simulate-drift` | 1 |
| 4 | `python 03_operations/page_generator/conformance.py --all` | 1 |
| 5 | `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short` | 0 |
| 6 | `python 03_operations/bsip1/core/test_enricher.py` | 0 |
| 7 | `python 03_operations/bsip2/proto_v0/src/run_router_regression.py` | 1 |
| 8 | `python 03_operations/bsip2/proto_v0/src/run_regression_check.py` | 0 |
| 9 | `python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short` | 0 |
| 10 | `python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py` | 0 |
| 11 | `python 03_operations/spine/smoke_test.py --dry-run` | 0 |

Note: router regression exit 1 (`dairy_flavor_contamination_biscuit`) is pre-existing on this worktree — unrelated to manifest tooling; not introduced by P473.

## Files changed

| file | action |
|------|--------|
| `03_operations/page_generator/live_manifest.py` | created |
| `03_operations/page_generator/live_manifest.json` | created |
| `03_operations/page_generator/conformance.py` | modified |
| `.github/workflows/barint_ci.yml` | modified |

```json
{
  "task": "P473",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/live_manifest.py", "action": "created", "sha256": "63006b87aef3f00c50a0708636fcdfb7f2a72316ca8c9d45a293cbd795e80f3f"},
    {"path": "03_operations/page_generator/live_manifest.json", "action": "created", "sha256": "7405e194133d0f7a7364844433e05e82d4f2589ddcfa8887478795f0c056c659"},
    {"path": "03_operations/page_generator/conformance.py", "action": "modified", "sha256": "970d78a4277fee84d528291f0bfb196e55108e8e7e5b3223a28028c47292c934"},
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "b639b2aa757aa008d60cbd38f87975e8c42b9e251b434d7c22bbd7743918c39f"}
  ],
  "counts": {
    "manifest_categories": "7/7 (live_manifest.json categories[] vs comparisonCategoryRegistry in registry/index.ts)",
    "manifest_gaps": "0/7 (categories with gaps[] field; live_manifest.json)",
    "manifest_catalog_registered": "7/7 (registered_in_catalog=true; live_manifest.json vs public-corpus-registry.ts slugs)",
    "conformance_stems_before": "18/18 (configs/*.json stems; histogram: 1 stem each, min/max=1/1; listed in table above)",
    "conformance_stems_after": "7/7 (manifest_config_stems; live_manifest.json + conformance.py --all)",
    "conformance_conforming": "5/7 (conformance.py --all; non_conforming=2 bread+cheese HARD-3; most_common outcome=conform)",
    "orphan_config_warns": "10/10 (live_manifest.py --check; most_common=1 warn per orphan; min/max warn count=1/1)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/live_manifest.py", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/live_manifest.py --check", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/live_manifest.py --check --simulate-drift", "exit_code": 1},
    {"cmd": "python 03_operations/page_generator/conformance.py --all", "exit_code": 1},
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short", "exit_code": 0},
    {"cmd": "python 03_operations/bsip1/core/test_enricher.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_router_regression.py", "exit_code": 1},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_regression_check.py", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py", "exit_code": 0},
    {"cmd": "python 03_operations/spine/smoke_test.py --dry-run", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P473_contract.md --root C:\\bari_wt_t466", "exit_code": 0}
  ],
  "not_done": [
    "rescore_all.py / spine_flip.py rewiring (listed as follow-up above)"
  ],
  "self_check": "live_manifest.py --check exits 0 on committed tree; --simulate-drift exits 1 with DRIFT error; conformance --all reads 7 manifest stems"
}
```